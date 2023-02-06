from math import exp, log
from copy import deepcopy


# add an engine input that contains Isp and Thrust to calculate with Stage.


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
    def __init__(self, type:str, engine_num:int, engine:Engine,  **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        
        self.type = type
        self.engine_num = engine_num
        self.engine = engine


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
        error = False
        error_message = 'You are missing: '
        if not hasattr(self, "type"):
            error_message +=  "type of propellant"
            error = True

        dV_SMF_pair = hasattr(self, "dV") and (hasattr(self, "SMF"))
        prop_struct_pair = hasattr(self, "m_propellant") and hasattr(self, "m_struct")

        if dV_SMF_pair and prop_struct_pair:
            raise Exception("Overconstrained!")

        if not dV_SMF_pair and not prop_struct_pair:
            error_message += "either the SMF-dV pair or the propellant-structural mass pair, "
            error = True
        
        if error == True:
            raise Exception(error_message[:len(error_message)-2] + '.')


class Rocket:
    def __init__(self, payload) -> None:
        '''
        Integral rocket that contains `Stage` objects to perform holistic calculations on flight parameters
        
        Parameter
        ---------
        payload:str
            Designed payload mass for the rocket
        
        Return
        ------
        NONE
        '''
        self.payload = payload
        self.stage = []
        self.original_stage = []

    def add_stage(self, stage, location = None):
        '''
        Add in stages to the rocket. If location is specifed, add the stage to the specified location in the rocket.
        If location not specified, add the stage to the top of the rocket.
        '''
        if location == None:
            self.original_stage.append(stage)
            self.stage.append(deepcopy(stage))
        else:
            self.original_stage.insert(location, stage)
            self.stage.insert(location, deepcopy(stage))
        self.calc()

    def delete_stage(self, location = None):
        '''
        Delete stages to the rocket. If location is specifed, deleted the rocket stage specified by the location.
        If location not specified, delete the top most stage of the rocket.
        '''
        if location == None:
            self.original_stage.pop()
            self.stage.pop()
        else:
            self.original_stage.pop(location)
            self.stage.pop(location)

        self.calc()

    def calc(self):
        '''
        calculate dependent rocket parameters and store them in rocket object based on which condition has been provided. 
        '''
        for i, og in enumerate(self.original_stage):
            self.stage[i] = deepcopy(og)

        #print(self.stage)
        for i in range(len(self.stage), 0, -1):
            curr = self.stage[i - 1]
            curr.m_stage = 0

        for i in range(len(self.stage), 0, -1):
            curr = self.stage[i - 1]
                
            if hasattr(curr, 'm_propellant') and hasattr(curr, 'm_struct'):
                curr.m_stage = curr.m_propellant + curr.m_struct
                curr.SMF = curr.m_struct/curr.m_stage
                curr.dV = 9.81 * curr.Isp * log((sum([o.m_stage for o in self.stage]) + self.payload)/(curr.m_struct + sum([o.m_stage for o in self.stage]) - curr.m_stage + self.payload))
                curr.mass_ratio = 1 / exp(curr.dV/(curr.Isp * 9.81))
            elif hasattr(curr, 'dV') and hasattr(curr, "SMF"):
                #in the situation this pair of two are specified.
                
                try:
                    mass = [o.m_stage for o in self.stage]
                except:
                    raise Exception("LMAO YOU don't have a mass yet")
                total_mass = self.payload + sum(mass)
                curr.m_struct = total_mass * (1 - 1/curr.mass_ratio)/(1/curr.mass_ratio - 1/curr.SMF)

                curr.m_propellant = curr.m_struct * (1/curr.SMF - 1)

                curr.m_stage = curr.m_struct + curr.m_propellant
                
            else:
                pass
                     
            
            #===================================================================
            #thrust calculations ↓
            curr.Fmin = curr.minTWR * curr.m_stage * 9.81 #in N
            curr.FperEngine = curr.Fmin/curr.engine_num #in N
            curr.m_dot = curr.Fmin/(curr.Isp * 9.81) #in kg/s
            curr.burntime = curr.m_propellant/curr.m_dot


        
        self.total_propellant_mass = sum([o.m_propellant for o in self.stage])
        self.total_struct_mass = sum([o.m_struct for o in self.stage]) + self.payload
        self.total_stage_mass = self.total_propellant_mass + self.total_struct_mass
        self.total_dV = sum([o.dV for o in self.stage])
    
    def __str__(self) -> str:
        string = ''
        for stage in self.stage:
            string += stage.__str__()

        attrs = vars(self)
        printing = ""
        for key in attrs:
            printing += f"{key}:{attrs[key]}\n"

        return string + printing
            


import yaml

if __name__ == "__main__":
    

    # stage_1 = UserDefinedStage(type = 'Hybrid', Isp = 300,  minTWR = 3, engine_num = 3, m_propellant = 5514.64366993181, m_struct = 681.585172688201)
    # stage_2 = UserDefinedStage(type = 'Methalox',Isp = 340,  minTWR = 1, engine_num = 1, m_propellant = 775.593887671062, m_struct = 115.893339537055)

    # Ryder = Rocket(payload = 140)
    # Ryder.add_stage(stage_1)
    # Ryder.add_stage(stage_2)
    
    # Ryder.delete_stage(0)
    
    # print(Ryder)
    # print("******************************************************")

    # Ryder.add_stage(stage_1, 0)
    # print(Ryder)
    # print("******************************************************")

    # stage_3 = UserDefinedStage(type = 'Hypergol', Isp = 320, engine_num = 1, minTWR = 1, m_propellant = 90, m_struct = 40)
    # Ryder.add_stage(stage_3)

    # print(Ryder)
    # print("******************************************************")




    Stryder_stage_1 = Stage(type = 'Hybrid', Isp = 300,  minTWR = 2, engine_num = 3, dV = 2000, SMF= 0.11) 

    #print(yaml.dump(Stryder_stage_1))
    Stryder_stage_2 = UserDefinedStage(type = 'Methalox',Isp = 340,  minTWR = 1.5, engine_num = 1, dV = 3500, SMF= 0.11) 
    #Stryder_stage_3 = Stage(type = 'Hypergol', Isp = 320,  minTWR = 0.8, engine_num = 1, dV = 3500,  SMF= 0.25) 

    stream = open('stage.yaml', 'r')
    kwargs = yaml.load(stream, Loader=yaml.CLoader)
    Stryder_stage_3 = UserDefinedStage(**kwargs[2])

    Stryder = Rocket(payload = 182)

    Stryder.add_stage(Stryder_stage_1) 
    Stryder.add_stage(Stryder_stage_2) 
    Stryder.add_stage(Stryder_stage_3) 
    

    
    print(Stryder)
    print("******************************************************")