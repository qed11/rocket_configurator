from math import exp, log
from copy import deepcopy

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