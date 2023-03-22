# Rural Medical Support System (RMSS) - Model Notes
This document presents the geernal notes related to the NetLogo model  developed as a part of the Georgia Institue of Technology - 2019 PMASE programs capstone project (`ASE6104 2021`). 

## Purpose
This model is created in support of the analysis for the RMSS. The model is intended to simulate the delivery system for the RMSS in sufficent detial to make some assumptios as to the efficacy of such a system. 

### Outline
The model is created using NetLogo 6.2.0. There are several agents within the model including: <br>

1. **Hubs:** represent the base location (central atlant: emory for instatance) for the medical stuffs (medicnine, blood, medical equpment).
    - message queue
    - charging station
    - status: waiting
2. **Hospitals**: represent rural locations that send messages to the hub for support. 
    - randomly placed for now
    - may have a charge station
    - status: idle, waiting
    - requests: standard, urgent, emergency
    
3. **Drones**: deliver the medical stuffs to the hospitals. 
    - chargeRate
    - discargeRate
    - speed
    - type
    - class
    - target
    - status: delivering, delivered, charging, charged, lost
    
4. **Sensors**: track the drone with `line-of-sight` (Not implemented Yet)




