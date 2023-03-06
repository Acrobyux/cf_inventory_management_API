Este proyecto es una API Rest desarrollada mediante Django REST framework que permite la administración de un sistema de inventario basado en ubicaciones (almacenes), se controlan altas y bajas

Consta de 5 Modelos:

  Warehouse: Representa una ubicacion (almacen) donde los productos pueden estar asignados.
  Category: Representa una division para organizar a los productos (un producto pertenece a una categoria).
  Product: Representa un producto que pertenece a una categoria y que puede estar presente en mas de un almacen distinto.
  Inventory: Representa el inventario fisico de un producto en un almacen especifico.
  Movement: Representa una transaccion de inventario, hay 3 tipos (In, Out, Transfer)
    Alta: Aumenta el stock de un producto en un determinado almacen.
    Baja: Decrementa el stock de un producto en un determinado almacen.
    Transferencia: Mueve el stock del almacen 'A' al almacen 'B'
  Se hacen validaciones de que se especifique un "almacen_origen" y "almacen_destino" segun sea el caso y que haya suficiente     stock para surtir una peticion de "Baja" o de "Transferencia" 
