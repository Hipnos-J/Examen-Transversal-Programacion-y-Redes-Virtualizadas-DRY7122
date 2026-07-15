vlan = int(input("Ingrese el rango de VLAN que consulta: "))

if 1 <= vlan <= 1005:
    print("La VLAN", vlan ,"corresponde al Rango Normal")
elif 1006 <= vlan <= 4094:
    print("La VLAN", vlan ,"corresponde al Rango Extendido")
else:
    print("La VLAN", vlan ,"esta Fuera del rango valido correspondiente o no es Válida")