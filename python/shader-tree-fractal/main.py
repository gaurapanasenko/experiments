#!/usr/bin/env python3

from pathlib import Path
from pyrr import Matrix44, Vector3
import struct
import numpy as np

import moderngl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.scene.camera import KeyboardCamera, OrbitCamera

RESERVE=4*4*2*4*10240


BUFFER = np.array([
     0,0,0,1, 0,0.5,0,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0
], dtype="f")
TRANSFORM = np.array([
    [[ 0.70710677*0.7, -0.70710677*0.7,  0.        ,  0         ],
      [ 0.70710677*0.7,  0.70710677*0.7, -0.        ,  0.        ],
      [-0.        ,  0.        ,  1.*0.7        ,  0.        ],
      [ 0        ,  0.5        ,  0.        ,  1        ]],
    [[ 0.70710677*0.7, 0.70710677*0.7,  0.        ,  0         ],
      [ -0.70710677*0.7,  0.70710677*0.7, -0.        ,  0.        ],
      [-0.        ,  0.        ,  1.*0.7        ,  0.        ],
      [ 0        ,  0.5        ,  0.        ,  1        ]],

    [[ 1.*0.7        , -0.        ,  0.        ,  0.        ],
      [ 0.        ,  0.70710677*0.7,  0.70710677*0.7,  0.        ],
      [-0.        , -0.70710677*0.7,  0.70710677*0.7,  0.        ],
      [ 0.        ,  0.5        ,  0.        ,  1        ]],

    [[ 1.*0.7        , -0.        ,  0.        ,  0.        ],
      [ 0.        ,  0.70710677*0.7, -0.70710677*0.7,  0.        ],
      [-0.        ,  0.70710677*0.7,  0.70710677*0.7,  0.        ],
      [ 0.        ,  0.5        ,  0.        ,  1        ]],


    # ~ [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]],
], dtype="f4")



TRANS_NUM = len(TRANSFORM)

class CameraWindow(mglw.WindowConfig):
    """Base class with built in 3D camera support"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(
            self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio,
            near=0.01, far=100.0,)
        self.camera_enabled = True
        self.camera.velocity = 1

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx/10, -dy/10)

    def resize(self, width: int, height: int):
        self.camera.projection.update(
            aspect_ratio=self.wnd.aspect_ratio)


class App(CameraWindow):
    title = "Tree L-system"
    resource_dir = (Path(__file__).parent / 'resources').resolve()
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.compute_shader = self.load_compute_shader(
            'affgen.glsl', defines={"TRANS_NUM": TRANS_NUM})
        self.compute_shader['trans'].write(TRANSFORM)
        self.verts_buffer = BUFFER
        self.vbo = self.ctx.buffer(None, reserve=RESERVE)

        self.prog = self.load_program("tree.glsl")
        self.prog['color'].value = 0.64, 0.45, 0.28, 1.0
        self.vao = self.ctx.vertex_array(self.prog, [
            (self.vbo, "4f", "in_position"),
        ])

        self.prog2 = self.load_program("leaf.glsl")
        self.prog2['color'].value = 0.3, 0.8, 0.3, 1.0
        self.leaf_vao = self.ctx.vertex_array(self.prog2, [
            (self.vbo, "4f", "in_position"),
        ])

        self.prog3 = self.load_program("cube_simple.glsl")
        self.prog3['color'].value = 0.1, 1.0, 0.1, 1.0
        self.cube = geometry.cube((100.0, .01, 100.0))

    def render(self, time, frametime):

        self.ctx.clear(0.3, 0.6, 0.9, 0.0)
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        iters = 1
        offset = 0
        sz = 0.07

        self.vbo.clear()
        self.vbo.write(self.verts_buffer)
        trans = Matrix44.from_translation((0, 0.5, 0), dtype='f4')
        trans *= Matrix44.from_eulers((0, np.pi/16 * np.sin(time*3), 0), dtype='f4')
        trans *= Matrix44.from_translation((0, -0.5, 0), dtype='f4')

        for i in range(8):
            self.vbo.bind_to_storage_buffer(0)
            self.vbo.bind_to_storage_buffer(1)
            # ~ rotation = Matrix44.from_eulers((0, np.pi/4, 0), dtype='f4') * rotation
            self.compute_shader["transform"].write(trans)
            self.compute_shader["in_offset"] = offset
            self.compute_shader["out_offset"] = offset + iters
            self.compute_shader.run(iters, 1, 1)
            self.prog['m_size'].value = sz
            offset += iters
            iters *= TRANS_NUM


        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_camera'].write(self.camera.matrix)
        self.prog2['m_proj'].write(self.camera.projection.matrix)
        self.prog2['m_camera'].write(self.camera.matrix)
        self.prog3['m_proj'].write(self.camera.projection.matrix)
        self.prog3['m_camera'].write(self.camera.matrix)

        self.prog3['m_model'].write(Matrix44.from_translation((0, -0.5, 0), dtype='f4'))
        self.cube.render(self.prog3)

        for i in range(7):
            for j in range(7):
                # ~ rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
                translation = Matrix44.from_translation((i, -0.5, -2 - j), dtype='f4')
                modelview = translation
                self.prog['m_model'].write(modelview)
                self.prog2['m_model'].write(modelview)

                iters = 1
                offset = 0
                sz = 0.07

                self.prog['m_size'].value = sz
                self.vao.render(mode=moderngl.LINES, vertices = 2, first=0)

                for _ in range(5):
                    offset += iters
                    iters *= TRANS_NUM
                    sz *= 0.5
                    self.prog['m_size'].value = sz
                    self.vao.render(mode=moderngl.LINES, vertices = 2*iters, first=2*offset)


                self.prog2['m_size'].value = sz * 7
                self.leaf_vao.render(mode=moderngl.POINTS, vertices = 2*iters, first=2*offset)

if __name__ == "__main__":
    mglw.run_window_config(App)
