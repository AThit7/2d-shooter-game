import pygame

class AssetManager:
    textures = {}
    sounds = {}
    def init():
        pygame.mixer.init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(16)

    def add_texture(texture_id, path):
        AssetManager.textures[texture_id] = pygame.image.load(path)

    def get_texture(texture_id):
        return AssetManager.textures[texture_id]

    def add_sound(sound_id, path, volume = 0.2):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        AssetManager.sounds[sound_id] = sound
    
    def play_sound(sound_id):
        AssetManager.sounds[sound_id].play()

