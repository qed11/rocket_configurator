import rocket_config.rocket
import rocket_config.stage

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




    Stryder_stage_1 = rocket_config.stage.UserDefinedStage(type = 'Hybrid', Isp = 300,  minTWR = 2, engine_num = 3, dV = 2000, SMF= 0.11) 

    #print(yaml.dump(Stryder_stage_1))
    Stryder_stage_2 = rocket_config.stage.UserDefinedStage(type = 'Methalox',Isp = 340,  minTWR = 1.5, engine_num = 1, dV = 3500, SMF= 0.11) 
    Stryder_stage_3 = rocket_config.stage.UserDefinedStage(type = 'Hypergol', Isp = 320,  minTWR = 0.8, engine_num = 1, dV = 3500,  SMF= 0.25) 

    Stryder = rocket_config.rocket.Rocket(payload = 182)

    Stryder.add_stage(Stryder_stage_1) 
    Stryder.add_stage(Stryder_stage_2) 
    Stryder.add_stage(Stryder_stage_3) 
    

    
    print(Stryder)
    print("******************************************************")