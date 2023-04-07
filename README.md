El invariante del monitor es: self.cars_in_bridge.value == 0 or (self.people_in_bridge.value == 0 and (self.cars_in_bridge.value <= 1 and (self.current_direction == direction)))
El puente es seguro porque cuando un coche o una persona quiere entrar al puente tiene que adquirir el mutex y comprobar si hay algún coche en el sentido opuesto o persona.
Tenemos ausencia de deadlocks porque el proceso que espera siempre libera el mutex antes de esperar en la cola y cuando lo hace se notifica a otro en la cola.
Tenemos ausencia de inanición porque cuando un proceso desea entrar al puente pero el invariante del monitor no se cumple, espera en la cola self.people_waiting y si lo abandona, se notifica a los procesos en la cola.
