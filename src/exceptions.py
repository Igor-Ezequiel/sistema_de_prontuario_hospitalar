class HospitalError(Exception):
   
    pass

class NaoEncontradoError(HospitalError):
   
    pass

class RegraDeNegocioError(HospitalError):
    
    pass

class PermissaoNegadaError(HospitalError):

    pass