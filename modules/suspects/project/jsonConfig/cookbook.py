'''Info Header Start
Name : cookbook
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.12000
Info Header End'''

from .config_module import *



resolution = CollectionDict({
    "Width" : ConfigValue(
        1920, 
        validator = lambda value: value > 1, 
        comment = "Width of the element as an Integer."),
    "Height" : ConfigValue(
        1080, 
        validator = lambda value: value > 1, 
        comment = "Height of the element as an Integer.")
    }, comment = "A 2D Resolution defined with integers.")

position = CollectionDict({
    "X" : ConfigValue(
        1.0, 
        parser = lambda value: float(value), 
        comment = "x Position."),
    "Y" : ConfigValue(
        1.0, 
        parser = lambda value: float(value), 
        comment = "x Position."),
})

from pathlib import Path
def file( filepath ):
    pathObject = Path( filepath )
    return EnumValue(
        "", allowedValues=[
            str(filepath) for filepath in pathObject.iterdir() if filepath.is_file()
        ]
    )

def folder( filepath ):
    pathObject = Path( filepath )
    return EnumValue(
        "", allowedValues=[
            str(filepath) for filepath in pathObject.iterdir() if filepath.is_dir()
        ]
    )

def fromParameter(parameter:Par, minMax = False):
    if parameter.style.lower() in ["float", "in",
                           "rgb", "rgba", 
                           "xy" "xyz", "xyzw",
                           "uv", "uvw", "wh"]:
        return ConfigValue(
            parameter.default,
            validator = (lambda value: parameter.min <= value <= parameter.max) if minMax else lambda value: True,
            comment = parameter.help
        )
    if parameter.style.lower() in ["menu", "strmenu"]:
        return EnumValue(
            parameter.default,
            allowedValues=[
                value for value in parameter.menuNames
            ]
        )
    return ConfigValue(
        str( parameter.default )
    )

def fromBlock( parBlock ):
    return CollectionDict({
        pargroup.name : fromParGroup( pargroup ) for pargroup in parBlock
    })

def fromSequence( pargroup:Sequence ):
    # Should we work us off of the existing items? Yeaah, think so.
    parsequence = pargroup.sequence
    return CollectionDict({
        str(index) : fromBlock( block ) for index,block in enumerate( parsequence.blocks )
    }, comment = pargroup.help)

def fromParGroup( pargroup:ParGroup ):
    if pargroup.isSequence: return fromSequence( pargroup )
    if len(pargroup) > 1: return CollectionDict({
        parameter.name : fromParameter( parameter ) 
        for parameter in pargroup
    })
    return fromParameter( pargroup[0] )

def fromCOMP( operator:COMP ):
    return CollectionDict({
        parGroup.name : fromParGroup( parGroup ) 
        for parGroup in operator.customParGroups if parGroup.isSequence or parGroup.sequence is None
       
    },  comment = operator.comment)