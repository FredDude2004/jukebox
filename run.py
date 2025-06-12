from app import create_app
import pygame

app = create_app()

if __name__ == '__main__':
    pygame.mixer.init()
    app.run(debug=True)
