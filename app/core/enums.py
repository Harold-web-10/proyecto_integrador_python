from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class MediaType(str, Enum):
    BOOK = "book"
    MOVIE = "movie"


class GenreEnum(str, Enum):
    FICCION = "ficcion"
    CIENCIA_FICCION = "ciencia_ficcion"
    FANTASIA = "fantasia"
    MISTERIO = "misterio"
    ROMANCE = "romance"
    TERROR = "terror"
    HISTORICO = "historico"
    AUTOAYUDA = "autoayuda"
    DISTOPICO = "distopico"
    REALISMO_MAGICO = "realismo_magico"
    JUVENIL = "juvenil"
    CLASICO = "clasico"
    POESIA = "poesia"
    NO_FICCION = "no_ficcion"
    BIOGRAFIA = "biografia"
    ENSAYO = "ensayo"
    ACCION = "accion"
    COMEDIA = "comedia"
    DRAMA = "drama"
    THRILLER = "thriller"
    SUSPENSE = "suspense"
    DOCUMENTAL = "documental"
    ANIMACION = "animacion"
    ANIME = "anime"
    AVENTURA = "aventura"
