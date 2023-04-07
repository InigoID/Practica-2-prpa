El invariante del monitor es: ((self.pedestrians.value > 0 and self.north_cars.value == 0 and self.south_cars.value == 0) or (self.pedestrians.value == 0 and (self.north_cars.value > 0 and self.south_cars.value == 0) or (self.north_cars.value == 0 and self.south_cars.value > 0))) and (self.waiting_north.value >= 0 and self.waiting_south.value >= 0 and self.waiting_pedestrians.value >= 0)

El puente es seguro gracias a las condiciones de espera self.bridge.wait_for ya que cuando un coche / peatón quiere entrar, se verifica antes si hay coches en la dirección opuesta / peatones en el puente.

Tenemos ausencia de deadlocks porque self.bridge.notify_all() avisa de cuando los coches o peatones salen del puente para que entren los siguientes en la cola.

Tenemos ausencia de inanición porque utiliza un sistema de turnos y cuando un proceso desea entrar al puente pero el invariante del monitor no se cumple, espera en la cola self.people_waiting y si lo abandona, se notifica a los procesos en la cola. 
