
import yaml
from rocket_stage_calc import Stage, UserDefinedStage, Rocket

if __name__ == '__main__':

    # Two different types of stages

    #`Stage` object passes in a very specific set of parameters. It performs the standard rocket computation similar to the spreadsheet
    Stryder_stage_1 = Stage(type = 'Hybrid', Isp = 300,  minTWR = 2, engine_num = 3, dV = 2000, SMF= 0.11) 

    #`UserDefinedStage` objects passes in user defined parameters, and based on provided parameters performs calculations. 
    Stryder_stage_2 = UserDefinedStage(type = 'Methalox',Isp = 340,  minTWR = 1.5, engine_num = 1, dV = 3500, SMF= 0.11) 
    
    # We can also implement using yaml and change parameters there. 
    stream = open('stage.yaml', 'r')
    kwargs = yaml.load(stream, Loader=yaml.CLoader)
    print(kwargs)
    Stryder_stage_3 = UserDefinedStage(**kwargs[0])

    #Note: Each stage checks if all required parameters are provided.

    # `Rocket` class puts together all the stages and performs calculations. 
    Stryder = Rocket(payload = 182)

    # Using `Stage.add_stage()` method, we adds rockets stages to specified location on the rocket. If location is not speficied,
    # it is defaulted to add the stage to the top of the existing stack
    # Each time a stage is added, the `Rocket` updates the parameters and calculates other dependent parameters. 
    Stryder.add_stage(Stryder_stage_1) 
    Stryder.add_stage(Stryder_stage_2) 
    Stryder.add_stage(Stryder_stage_3) 
    


    with open("stryder.yaml", "w") as f:

        f.write(yaml.dump(Stryder))

