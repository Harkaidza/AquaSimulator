import random
from os import system

import glfw
import pygame

import ShaderLoader
import TextureLoader

from OpenGL.GL import *
from ObjLoader import *
from pygame import *

from Camera import Camera
from pyrr import matrix44, Vector3, Matrix44

import numpy as np

pygame.init()
#pygame.mixer.music.load("sound/Sound_water.mp3")
pygame.mixer.music.load("sound/AquaDisco.mp3")


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


cam = Camera()
keys = [False] * 1024
w_width, w_height = 1280, 720
lastX, lastY = w_width / 2, w_height / 2
first_mouse = True


def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key < 0 or key >= 1024:
        return
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def do_movement():
    if keys[glfw.KEY_UP]:
        cam.process_keyboard("FORWARD", 0.05)
    if keys[glfw.KEY_DOWN]:
        cam.process_keyboard("BACKWARD", 0.05)
    if keys[glfw.KEY_LEFT]:
        cam.process_keyboard("LEFT", 0.05)
    if keys[glfw.KEY_RIGHT]:
        cam.process_keyboard("RIGHT", 0.05)


def mouse_callback(window, x_pos, y_pos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = x_pos
        lastY = y_pos
        first_mouse = False

    x_offset = x_pos - lastX
    y_offset = lastY - y_pos

    lastX = x_pos
    lastY = y_pos

    cam.process_mouse_movement(x_offset, y_offset)


def models_drawing(models_vao, models_tex, model_loc, models_model, models):
    glBindVertexArray(models_vao)
    glBindTexture(GL_TEXTURE_2D, models_tex)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, models_model)
    glDrawArrays(GL_TRIANGLES, 0, len(models.vertex_index))
    glBindVertexArray(0)


def pos_tex_normal(model, model_texture_offset, model_normal_offset):
    model_vao = glGenVertexArrays(1)
    glBindVertexArray(model_vao)
    model_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, model_vbo)
    glBufferData(GL_ARRAY_BUFFER, model.model.itemsize * len(model.model), model.model, GL_STATIC_DRAW)
    # position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, model.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, model.model.itemsize * 2, ctypes.c_void_p(model_texture_offset))
    glEnableVertexAttribArray(1)
    # normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, model.model.itemsize * 3, ctypes.c_void_p(model_normal_offset))
    glEnableVertexAttribArray(2)
    glBindVertexArray(0)
    return model_vao, model_vbo


def obj_load(s1, s2):
    model = ObjLoader()
    model.load_model(s1)
    model_tex = TextureLoader.load_texture(s2)
    model_texture_offset = len(model.vertex_index) * 12
    model_normal_offset = model_texture_offset + len(model.texture_index) * 8
    return model, model_tex, model_texture_offset, model_normal_offset


def main():
    if not glfw.init():
        return

    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "Aqua-simulator (Computer graphics)", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # --------------------------------------------------------------
    fish, fish_tex, fish_texture_offset, fish_normal_offset = \
        obj_load("models/fish/fish.obj", "models/fish/fish.jpg")

    plato, plato_tex, plato_texture_offset, plato_normal_offset = \
         obj_load("models/plato/plato.obj", "models/plato/plato.png")
    # obj_load("models/putin/putin.obj", "models/putin/putin.png")

    floor, floor_tex, floor_texture_offset, floor_normal_offset = \
        obj_load("models/floor/floor.obj", "models/floor/floor.png")

    shark, shark_tex, shark_texture_offset, shark_normal_offset = \
        obj_load("models/shark/shark.obj", "models/shark/shark.png")

    meduza, meduza_tex, meduza_texture_offset, meduza_normal_offset = \
        obj_load("models/meduza/meduza.obj", "models/meduza/meduza.png")

    grass, grass_tex, grass_texture_offset, grass_normal_offset = \
        obj_load("models/grass/grass.obj", "models/grass/grass.png")

    crab, crab_tex, crab_texture_offset, crab_normal_offset = \
        obj_load("models/crab/crab.obj", "models/crab/crab.png")

    sea_ezg, sea_ezg_tex, sea_ezg_texture_offset, sea_ezg_normal_offset = \
        obj_load("models/sea_ezg/sea_ezg.obj", "models/sea_ezg/sea_ezg.png")

    fish2, fish2_tex, fish2_texture_offset, fish2_normal_offset = \
        obj_load("models/fish2/fish2.obj", "models/fish2/fish2.png")

    fish3, fish3_tex, fish3_texture_offset, fish3_normal_offset = \
        obj_load("models/fish3/fish3.obj", "models/fish3/fish3.png")

    star, star_tex, star_texture_offset, star_normal_offset = \
        obj_load("models/star/star.obj", "models/star/star.png")
    # --------------------------------------------------------------

    generic_shader = ShaderLoader.compile_shader("shaders/generic_vertex_shader.vs",
                                                 "shaders/generic_fragment_shader.fs")

    fish_vao, fish_vbo = pos_tex_normal(fish, fish_texture_offset, fish_normal_offset)
    fish2_vao, fish2_vbo = pos_tex_normal(fish2, fish2_texture_offset, fish2_normal_offset)
    fish3_vao, fish3_vbo = pos_tex_normal(fish3, fish3_texture_offset, fish3_normal_offset)
    shark_vao, shark_vbo = pos_tex_normal(shark, shark_texture_offset, shark_normal_offset)

    floor_vao, floor_vbo = pos_tex_normal(floor, floor_texture_offset, floor_normal_offset)
    plato_vao, plato_vbo = pos_tex_normal(plato, plato_texture_offset, plato_normal_offset)
    grass_vao, grass_vbo = pos_tex_normal(grass, grass_texture_offset, grass_normal_offset)
    
    meduza_vao, meduza_vbo = pos_tex_normal(meduza, meduza_texture_offset, meduza_normal_offset)
    crab_vao, crab_vbo = pos_tex_normal(crab, crab_texture_offset, crab_normal_offset)
    sea_ezg_vao, sea_ezg_vbo = pos_tex_normal(sea_ezg, sea_ezg_texture_offset, sea_ezg_normal_offset)
    star_vao, star_vbo = pos_tex_normal(star, star_texture_offset, star_normal_offset)
    

    glClearColor(0, 0.1, 0.5, 1)
    glEnable(GL_DEPTH_TEST)

    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    fish_model = matrix44.create_from_translation(Vector3([-4.0, 4.0, -10.0]))
    shark_model = matrix44.create_from_translation(Vector3([0.0, 8.0, -12.0]))

    plato_model = matrix44.create_from_translation(Vector3([0.0, 3.5, 3.5]))
    floor_model = matrix44.create_from_translation(Vector3([0.0, 0.0, 0.0]))

    meduza_all = np.array([
        matrix44.create_from_translation(Vector3([5.0, 4.0, 14.0])),
        matrix44.create_from_translation(Vector3([7.0, 6.0, 15.0]))
    ])

    for i in range(7):
        x = random.uniform(-8.0, 16.0)
        y = random.uniform(-10.0, 20.0)
        z = random.uniform(3.0, 10.0)
        meduza_all = np.append(meduza_all, [matrix44.create_from_translation(Vector3([x, z, y]))], axis=0)

    grass_all = np.array([
        matrix44.create_from_translation(Vector3([0.9, 0.25, 0.5])),
        matrix44.create_from_translation(Vector3([0.5, 0.25, 0.5])),
        matrix44.create_from_translation(Vector3([0.7, 0.25, 0.3])),
        matrix44.create_from_translation(Vector3([0.10, 0.25, 0.8])),
        matrix44.create_from_translation(Vector3([-3.0, 0.25, 4.0]))
    ])

    for i in range(15):
        x = random.uniform(-5.0, 5.0)
        y = random.uniform(-5.0, 5.0)
        grass_all = np.append(grass_all, [matrix44.create_from_translation(Vector3([x, 0.25, y]))], axis=0)

    star_model = np.array([matrix44.create_from_translation(Vector3([5.12, 0.1, 5.5]))])
    for i in range(8):
        x = random.uniform(-5.0, 5.0)
        y = random.uniform(-5.0, 5.0)
        star_model = np.append(star_model, [matrix44.create_from_translation(Vector3([x, 0.1, y]))], axis=0)

    crab_model = matrix44.create_from_translation(Vector3([0.12, 0.244, 0.5]))

    sea_ezg_all = np.array([
        matrix44.create_from_translation(Vector3([0.7, 0.16, 0.9])),
        matrix44.create_from_translation(Vector3([-0.3, 0.16, 1.5])),
        matrix44.create_from_translation(Vector3([1.7, 0.16, 1.7]))
    ])

    fish2_model = np.array([
        matrix44.create_from_translation(Vector3([3.0, 5.0, 14.0])),
        matrix44.create_from_translation(Vector3([4.0, 6.0, 13.0])),
        matrix44.create_from_translation(Vector3([6.0, 4.0, 10.0]))
    ])

    fish3_model = np.array([
        matrix44.create_from_translation(Vector3([-8.0, 4.2, 8.0])),
        matrix44.create_from_translation(Vector3([-3.0, 6.0, 9.0])),
        matrix44.create_from_translation(Vector3([5.0, 6.3, 11.5])),
        matrix44.create_from_translation(Vector3([7.0, 5.3, 13.5])),
        matrix44.create_from_translation(Vector3([6.0, 7.3, 12.5]))
    ])

    glUseProgram(generic_shader)
    model_loc = glGetUniformLocation(generic_shader, "model")
    view_loc = glGetUniformLocation(generic_shader, "view")
    proj_loc = glGetUniformLocation(generic_shader, "proj")
    light_loc = glGetUniformLocation(generic_shader, "lightPos")
    view_pos_loc = glGetUniformLocation(generic_shader, "viewPos")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniform3fv(light_loc, 1, (5.0, 10.0, 50.0))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)

    pygame.mixer.music.play(not (glfw.window_should_close(window)))
    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        glUniform3fv(view_pos_loc, 1, (cam.camera_pos.x, cam.camera_pos.y, cam.camera_pos.z))

        rot_1 = Matrix44.from_y_rotation(glfw.get_time() * 0.3)
        rot_2 = Matrix44.from_y_rotation(glfw.get_time() * 0.7).inverse
        rot_3 = Matrix44.from_y_rotation(glfw.get_time() * 0.01).inverse

        scale_1 = Matrix44.from_scale(np.array([1000.0, 1.0, 1000.0]))

        models_drawing(fish_vao, fish_tex, model_loc, rot_1 * fish_model, fish)
        models_drawing(shark_vao, shark_tex, model_loc, rot_2 * shark_model, shark)
        models_drawing(floor_vao, floor_tex, model_loc, scale_1 * floor_model, floor)

        # scale_2 = Matrix44.from_scale(np.array([0.3, 0.3, 0.3]))
        models_drawing(plato_vao, plato_tex, model_loc, plato_model, plato)

        for i in range(len(meduza_all)):
            if i > 1:
                if i % 2 == 0:
                    scale_2 = Matrix44.from_scale(np.array([0.5, 0.5, 0.5]))
                    models_drawing(meduza_vao, meduza_tex, model_loc, scale_2 * meduza_all[i], meduza)
                else:
                    scale_2 = Matrix44.from_scale(np.array([0.8, 0.8, 0.8]))
                    models_drawing(meduza_vao, meduza_tex, model_loc, scale_2 * meduza_all[i], meduza)
            else:
                models_drawing(meduza_vao, meduza_tex, model_loc, meduza_all[i], meduza)

        scale_2 = Matrix44.from_scale(np.array([7.0, 7.0, 7.0]))
        for i in range(len(grass_all)):
            models_drawing(grass_vao, grass_tex, model_loc, scale_2 * grass_all[i], grass)

        scale_2 = Matrix44.from_scale(np.array([12.0, 12.0, 12.0]))
        models_drawing(crab_vao, crab_tex, model_loc, rot_3 * scale_2 * crab_model, crab)

        for i in range(len(sea_ezg_all)):
            if i == 0:
                scale_2 = Matrix44.from_scale(np.array([5.0, 5.0, 5.0]))
            else:
                scale_2 = Matrix44.from_scale(np.array([3.0, 3.0, 3.0]))
            models_drawing(sea_ezg_vao, sea_ezg_tex, model_loc, scale_2 * sea_ezg_all[i], sea_ezg)

        rot_2 = Matrix44.from_y_rotation(glfw.get_time() * 0.25)
        for i in range(len(fish2_model)):
            models_drawing(fish2_vao, fish2_tex, model_loc, rot_2 * fish2_model[i], fish2)

        rot_2 = Matrix44.from_y_rotation(glfw.get_time() * 0.15)
        for i in range(len(fish3_model)):
            models_drawing(fish3_vao, fish3_tex, model_loc, rot_2 * fish3_model[i], fish3)

        scale_2 = Matrix44.from_scale(np.array([3.3, 3.3, 3.3]))
        for i in range(len(star_model)):
            models_drawing(star_vao, star_tex, model_loc, scale_2 * star_model[i], grass)

        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()


