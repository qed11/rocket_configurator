from math import exp, log
from copy import deepcopy


class Engine:
    def __init__(self, Isp, mass, thrust = None) -> None:
        self.Isp = Isp
        self.mass = mass
        self.thrust = thrust
        

class UserDefinedStage:
    '''
    This is a user defined stage, where you can specify any parameters. 
    It behaves just like a `Stage` object, but allowing the user to have more freedom in choosing different configurations
    of the rocket to test.
    
    Parameters:
    -------------

        **kwargs:
            rocket design parameters

        Mandatory kwargs:
            Isp: type
                Specific impulse of the rocket propellant


            type:str
                Type of engine that is used in this stage
            
            
            minTWR:float
                minimum thrust to weight ratio for the rocket stage
            

            engine_num:float
                number of engines that exists in this stage of the rocket
        
        
        It also must have one of the following pair of parameters
            
            
            dV - SMF pair
                
                
                dV:float
                    target delta-V for the rocket stage


                SMF:float
                    structural mass fraction of the stage. mathematically, SMF = m_dry/m_wet

        
            propellant - structural mass


                m_struct:float
                    designed structural mass of the rocket stage


                m_propellant:float
                    designed propellant mass



        Return
        --------------
        NONE
    '''
    def __init__(self, Isp:int, type:str, engine_num:int, minTWR:float,  **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        
        self.Isp = Isp
        self.type = type
        self.engine_num = engine_num
        self.minTWR = minTWR


        if hasattr(self, "dV") and hasattr(self, "Isp"):
            try:
                self.mass_ratio = 1 / exp(self.dV/(self.Isp * 9.81))
            except:
                raise Exception("Can't define this attribute")
        
        self.error_check()

    def __str__(self) -> str:
        separation = '============================================\n'
        attrs = vars(self)
        printing = ""
        for key in attrs:
            printing += f"{key}:{attrs[key]}\n"
        return separation + printing + separation
    
    def error_check(self):
        '''
        This is an error checking function. It will return an error if mandatory parameters are not provided.
        Mandatory parameters are:

        - Type of the rocket fuel
        - Specific impulse
        - Number of engines
        - Minimum thrust to weight ratio
        
        Moreover, the user must:
        - Either specify dV and assumed strucutral mass fraction, or
        - Specify the mass of the structure and propellant. 
        '''

        dV_SMF_pair = hasattr(self, "dV") and (hasattr(self, "SMF"))
        prop_struct_pair = hasattr(self, "m_propellant") and hasattr(self, "m_struct")

        if dV_SMF_pair and prop_struct_pair:
            raise Exception("Overconstrained!")

        if not dV_SMF_pair and not prop_struct_pair:
            error_message = "You are missing either the SMF-dV pair or the propellant-structural mass pair."
            
            print(error_message)


        

