

# Validating the required Information
def required_info_Validation(data):
    requiredVarientInfo = ['size', 'units', 'price', 'color']
    for vInfoReq in requiredVarientInfo:
        if not vInfoReq in data:
            return False, f"Informacion requerida {vInfoReq}"
        if vInfoReq == "":
            return False, f"Informacin Requerida, {vInfoReq} no debe estar blanco"
    
    return True, ""


def cleanString(uncleanString):
    cleanedString = uncleanString.strip().title().replace(".", "").replace(",", "")
    return cleanedString


def info_require_for_update(varId, data):
    if varId == "":
        return False, "no debe estar en blanco"
    if not data:
        return False, "Informacion no debe estar en blanco"
    
    return True, ""
