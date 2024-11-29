# move_player.py
from panda3d.core import LVector3, LVector2, ClockObject


def move_player(camera, controls, cTrav, render, player):
    key_map = controls.key_map
    speed = 5 * ClockObject.getGlobalClock().getDt()
    direction = LVector3(0, 0, 0)

    if key_map["forward"]:
        direction.y += speed
    if key_map["backward"]:
        direction.y -= speed
    if key_map["left"]:
        direction.x -= speed
    if key_map["right"]:
        direction.x += speed

    forward_vec = LVector2(camera.getQuat().getForward().getX(),
                           camera.getQuat().getForward().getY()).normalized()
    right_vec = LVector2(camera.getQuat().getRight().getX(),
                         camera.getQuat().getRight().getY()).normalized()

    # Combine les vecteurs de direction (horizontalement)
    move_vec = forward_vec * direction.y + right_vec * direction.x
    move_vec_3d = LVector3(move_vec.getX(), move_vec.getY(), 0)

    # Calcul de la nouvelle position
    new_position = camera.getPos() + move_vec_3d

    # Ajuste la hauteur en fonction du raycast
    cTrav.traverse(render)
    entries = list(player.ray_queue.entries)
    entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

    if entries:
        ground_z = entries[0].getSurfacePoint(render).getZ()
        new_position.z = ground_z + 1

    camera.setPos(new_position)
