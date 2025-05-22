import os

class Config:
    PORT = os.environ.get('PORT') or 80
    