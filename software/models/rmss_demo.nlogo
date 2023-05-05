extensions [data]

to setup
  clear-all
  
  ;; Load JSON data from file
  let json-data data:from-file "rmss_b1.json"
  
  ;; Extract hospital data from JSON and create hospitals
  foreach data:find-nodes "//*[name()='hospital']" json-data [
    let remote-type data:get "remoteType/parameter/value" ?
    let med-count data:get "medCount/parameter/value" ?
    let loc-x data:get "locX/parameter/value" ?
    let loc-y data:get "locY/parameter/value" ?
    
    create-hospitals 1 [
      set remoteType remote-type
      set medCount med-count
      setxy loc-x loc-y
    ]
  ]
  
  ;; Extract drone data from JSON and create drones
  foreach data:find-nodes "//*[name()='']/attribute::*[name()='emergencyResponseTime' or name()='standardResponseTime']" json-data [
    let response-time data:get "parameter/value" ?
    
    create-drones 1 [
      ifelse data:get "name" (data:get-parent "name" ?) = "emergencyResponseTime"
      [ set emergencyResponseTime response-time ]
      [ set standardResponseTime response-time ]
    ]
  ]
  
  reset-ticks
end
