import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { PROVENANCE_STYLE, type Part, type Provenance, type ReferenceCamera } from './model';

interface Props {
  assetUrl: string;
  parts: Map<string, Part>;
  hiddenSystems: Set<string>;
  hiddenProvenance: Set<Provenance>;
  selected: string | null;
  onSelect: (partId: string | null) => void;
  onLoaded: (info: { triangles: number }) => void;
  pose: ReferenceCamera | null;
  poseNonce: number;
}

const SELECTION_COLOR = new THREE.Color(0xff5c8a);

/**
 * three.js scene. Provenance is drawn into the geometry: opacity and an outline style per state,
 * and the filter HIDES rather than fades — a faded outline is still a shape a reader will trace.
 */
export default function BridgeViewer(props: Props) {
  const mountRef = useRef<HTMLDivElement>(null);
  const stateRef = useRef<{
    renderer: THREE.WebGLRenderer;
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera | THREE.OrthographicCamera;
    perspective: THREE.PerspectiveCamera;
    orthographic: THREE.OrthographicCamera;
    controls: OrbitControls;
    root: THREE.Object3D | null;
    outlines: Map<string, THREE.LineSegments>;
    orthoHeight: number;
    disposed: boolean;
  } | null>(null);

  // --- one-time scene setup
  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    // An explicit initial size: a headless page may never fire ResizeObserver, and a canvas sized
    // only from that reports zero width and screenshots fail.
    renderer.setSize(mount.clientWidth || 1280, mount.clientHeight || 720, false);
    mount.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0e1116);

    const camera = new THREE.PerspectiveCamera(42, 16 / 9, 1, 20000);
    camera.position.set(-620, 340, 900);

    // A second, orthographic camera. The HAER measured drawing is an orthographic elevation, so an
    // overlay against it is only meaningful if the model can be projected the same way.
    const ortho = new THREE.OrthographicCamera(-100, 100, 100, -100, -10000, 20000);
    ortho.position.copy(camera.position);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.target.set(0, 60, 0);

    scene.add(new THREE.HemisphereLight(0xdfe7f2, 0x1a1d22, 1.5));
    const key = new THREE.DirectionalLight(0xffffff, 1.6);
    key.position.set(-400, 700, 600);
    scene.add(key);

    // Mean high water. The datum is declared, not converted — GEOMETRY-CONTROL.md section 1.
    const water = new THREE.Mesh(
      new THREE.PlaneGeometry(4000, 1200),
      new THREE.MeshBasicMaterial({ color: 0x16344a, transparent: true, opacity: 0.55 }),
    );
    water.rotation.x = -Math.PI / 2;
    scene.add(water);

    const grid = new THREE.GridHelper(4000, 40, 0x2a3442, 0x1b222c);
    scene.add(grid);

    stateRef.current = {
      renderer,
      scene,
      camera,
      perspective: camera,
      orthographic: ortho,
      controls,
      root: null,
      outlines: new Map(),
      orthoHeight: 300,
      disposed: false,
    };

    let frame = 0;
    const tick = () => {
      const st = stateRef.current;
      if (!st || st.disposed) return;
      st.controls.update();
      st.renderer.render(st.scene, st.camera);
      frame = requestAnimationFrame(tick);
    };
    tick();

    const resize = () => {
      const st = stateRef.current;
      if (!st) return;
      const w = mount.clientWidth || 1280;
      const h = mount.clientHeight || 720;
      const aspect = w / h;
      st.perspective.aspect = aspect;
      st.perspective.updateProjectionMatrix();
      const halfH = st.orthoHeight / 2;
      const halfW = halfH * aspect;
      st.orthographic.left = -halfW;
      st.orthographic.right = halfW;
      st.orthographic.top = halfH;
      st.orthographic.bottom = -halfH;
      st.orthographic.updateProjectionMatrix();
      st.renderer.setSize(w, h, false);
    };
    resize();
    const observer = new ResizeObserver(resize);
    observer.observe(mount);
    window.addEventListener('resize', resize);

    return () => {
      const st = stateRef.current;
      if (st) st.disposed = true;
      cancelAnimationFrame(frame);
      observer.disconnect();
      window.removeEventListener('resize', resize);
      renderer.dispose();
      if (renderer.domElement.parentElement === mount) mount.removeChild(renderer.domElement);
    };
  }, []);

  // --- load / reload the asset
  useEffect(() => {
    const st = stateRef.current;
    if (!st) return;
    let cancelled = false;

    new GLTFLoader().load(new URL(props.assetUrl, document.baseURI).toString(), (gltf) => {
      if (cancelled || !stateRef.current) return;
      const state = stateRef.current;
      if (state.root) state.scene.remove(state.root);
      state.outlines.clear();

      let triangles = 0;
      const ownerOf = (obj: THREE.Object3D): Part | undefined => {
        let node: THREE.Object3D | null = obj;
        while (node) {
          const part = props.parts.get(node.name);
          if (part) return part;
          node = node.parent;
        }
        return undefined;
      };

      gltf.scene.traverse((obj) => {
        if (!(obj instanceof THREE.Mesh)) return;
        const geometry = obj.geometry as THREE.BufferGeometry;
        const index = geometry.getIndex();
        if (index) triangles += index.count / 3;
        // Resolve through ancestors: a multi-primitive part arrives as a Group whose Mesh children
        // carry generated names, so matching on the mesh name alone would skip its styling.
        const part = ownerOf(obj);
        if (!part) return;

        const style = PROVENANCE_STYLE[part.provenance];
        const material = obj.material as THREE.MeshStandardMaterial;
        material.transparent = style.opacity < 1;
        material.opacity = style.opacity;
        material.depthWrite = style.opacity >= 1;

        // Outline overlay. LineDashedMaterial silently renders solid without computeLineDistances().
        const edges = new THREE.EdgesGeometry(geometry, 25);
        const lineMaterial =
          style.outline === 'solid'
            ? new THREE.LineBasicMaterial({ color: 0xdfe7f2, transparent: true, opacity: 0.9 })
            : new THREE.LineDashedMaterial({
                color: 0xdfe7f2,
                dashSize: style.dash,
                gapSize: style.gap,
                transparent: true,
                opacity: style.outline === 'dotted' ? 0.5 : 0.75,
              });
        const outline = new THREE.LineSegments(edges, lineMaterial);
        if (style.outline !== 'solid') outline.computeLineDistances();
        outline.name = `${obj.name}__outline`;
        obj.add(outline);
        state.outlines.set(part.part_id, outline);
      });

      state.root = gltf.scene;
      state.scene.add(gltf.scene);
      props.onLoaded({ triangles: Math.round(triangles) });
    });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.assetUrl, props.parts]);

  // --- filters: hide, do not fade
  useEffect(() => {
    const st = stateRef.current;
    if (!st?.root) return;
    // Match on any Object3D, not only Mesh: a part with more than one primitive is loaded as a
    // Group whose children carry generated names, so a Mesh-only pass silently leaves it visible.
    st.root.traverse((obj) => {
      const part = props.parts.get(obj.name);
      if (!part) return;
      obj.visible =
        !props.hiddenSystems.has(part.system) && !props.hiddenProvenance.has(part.provenance);
    });
  }, [props.hiddenSystems, props.hiddenProvenance, props.parts, props.assetUrl]);

  // --- selection highlight
  useEffect(() => {
    const st = stateRef.current;
    if (!st?.root) return;
    st.root.traverse((obj) => {
      if (!(obj instanceof THREE.Mesh)) return;
      let node: THREE.Object3D | null = obj;
      while (node && !props.parts.has(node.name)) node = node.parent;
      if (!node) return;
      const material = obj.material as THREE.MeshStandardMaterial;
      if (!material.userData.baseColor) {
        material.userData.baseColor = material.color.clone();
      }
      material.color.copy(
        props.selected === node.name ? SELECTION_COLOR : (material.userData.baseColor as THREE.Color),
      );
    });
  }, [props.selected, props.parts, props.assetUrl]);

  // --- apply a reference view's camera pose
  //
  // Poses are authored in the model's Z-up frame (GEOMETRY-CONTROL.md section 1). The GLB root
  // carries the Z-up to Y-up rotation, so a pose must be converted the same way before it is
  // handed to the camera: (x, y, z) -> (x, z, -y). Doing this here, once, keeps every pose in
  // reference-views.json readable against the control document.
  useEffect(() => {
    const st = stateRef.current;
    const mount = mountRef.current;
    if (!st || !mount || !props.pose) return;
    const pose = props.pose;

    const toRender = (v: readonly number[]) => new THREE.Vector3(v[0], v[2], -v[1]);
    const eye = toRender(pose.position);
    const target = toRender(pose.target);
    const up = toRender(pose.up ?? [0, 0, 1]).normalize();

    const aspect = (mount.clientWidth || 1280) / (mount.clientHeight || 720);
    let camera: THREE.PerspectiveCamera | THREE.OrthographicCamera;
    if (pose.projection === 'orthographic') {
      const halfH = (pose.ortho_height_m ?? 300) / 2;
      st.orthoHeight = pose.ortho_height_m ?? 300;
      st.orthographic.left = -halfH * aspect;
      st.orthographic.right = halfH * aspect;
      st.orthographic.top = halfH;
      st.orthographic.bottom = -halfH;
      st.orthographic.updateProjectionMatrix();
      camera = st.orthographic;
    } else {
      st.perspective.fov = pose.fov_y_deg ?? 42;
      st.perspective.aspect = aspect;
      st.perspective.updateProjectionMatrix();
      camera = st.perspective;
    }

    camera.position.copy(eye);
    camera.up.copy(up);
    camera.lookAt(target);

    if (st.camera !== camera) {
      st.camera = camera;
      st.controls.object = camera;
    }
    st.controls.target.copy(target);
    st.controls.update();
  }, [props.pose, props.poseNonce]);

  // --- picking
  useEffect(() => {
    const st = stateRef.current;
    const mount = mountRef.current;
    if (!st || !mount) return;
    const raycaster = new THREE.Raycaster();
    raycaster.params.Line = { threshold: 3 };

    const onClick = (event: MouseEvent) => {
      const state = stateRef.current;
      if (!state?.root) return;
      const rect = state.renderer.domElement.getBoundingClientRect();
      const pointer = new THREE.Vector2(
        ((event.clientX - rect.left) / rect.width) * 2 - 1,
        -((event.clientY - rect.top) / rect.height) * 2 + 1,
      );
      raycaster.setFromCamera(pointer, state.camera);
      const hits = raycaster.intersectObject(state.root, true);
      for (const hit of hits) {
        let node: THREE.Object3D | null = hit.object;
        while (node && !props.parts.has(node.name)) node = node.parent;
        if (node && node.visible) {
          props.onSelect(node.name);
          return;
        }
      }
      props.onSelect(null);
    };

    mount.addEventListener('click', onClick);
    return () => mount.removeEventListener('click', onClick);
  }, [props.parts, props.onSelect]);

  return <div className="viewport" ref={mountRef} data-testid="viewport" />;
}
