import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Asegurar de que numpy está instalado
try:
    import numpy as np
    print("NumPy ya está instalado.")
except ImportError:
    print("NumPy no está instalado. Instalando...")
    install_package('numpy')
    import numpy as np

# Asegurar de que tenseal está instalado
try:
    import tenseal as ts
    print("TenSEAL ya está instalado.")
except ImportError:
    print("TenSEAL no está instalado. Instalando...")
    install_package('tenseal')
    import tenseal as ts

def main():
    print("Step 1: Configurando el contexto de cifrado...\n")
    # Parámetros de la encriptación
    poly_mod_degree = 8192
    coeff_mod_bit_sizes = [60, 40, 40, 60]

    # Crear contexto de encriptación
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_mod_degree,
        coeff_mod_bit_sizes
    )

    # Habilitar el guardado de claves públicas y de evaluación
    context.global_scale = 2**40
    context.generate_galois_keys()
    context.generate_relin_keys()

    print("Contexto de cifrado configurado.\n")

    # Datos de pacientes del hospital 1 y 2
    hospital_1_data = [110, 105, 120]
    hospital_2_data = [130, 115, 100]

    print("Step 2: Mostrando datos originales...")
    print("Datos: Glucosa 3 pacientes del hospital ABC:", hospital_1_data)
    print("Datos: Glucosa 3 pacientes del hospital DEF:", hospital_2_data, "\n")

    print("Step 3: Cifrando datos de pacientes...\n")
    # Convertir datos a tensores y cifrarlos
    hospital_1_encrypted = ts.ckks_vector(context, hospital_1_data)
    hospital_2_encrypted = ts.ckks_vector(context, hospital_2_data)

    # Convertir a lista para visualización
    hospital_1_encrypted_list = hospital_1_encrypted.serialize()
    hospital_2_encrypted_list = hospital_2_encrypted.serialize()

    print("Datos cifrados del hospital ABC (parcial):", hospital_1_encrypted_list[:10], "...\n")
    print("Datos cifrados del hospital DEF (parcial):", hospital_2_encrypted_list[:10], "...\n")

    print("Step 4: Sumando datos cifrados...\n")
    sum_encrypted = hospital_1_encrypted + hospital_2_encrypted

    # Convertir a lista para visualización
    sum_encrypted_list = sum_encrypted.serialize()
    print("Datos cifrados después de la suma (parcial):", sum_encrypted_list[:10], "...\n")

    print("Step 5: Descifrando la suma...\n")
    sum_decrypted = sum_encrypted.decrypt()
    print("Suma de niveles de glucosa (descifrada):", sum_decrypted, "\n")

    # Número total de pacientes
    total_patients = len(hospital_1_data) + len(hospital_2_data)

    print("Step 6: Calculando promedio cifrado...\n")
    average_encrypted = sum_encrypted * (1 / total_patients)

    # Convertir a lista para visualización
    average_encrypted_list = average_encrypted.serialize()
    print("Datos cifrados del promedio (parcial):", average_encrypted_list[:10], "...\n")

    print("Step 7: Descifrando el promedio...\n")
    average_decrypted = average_encrypted.decrypt()
    print("Promedio de niveles de glucosa (descifrado):", average_decrypted, "\n")
    print("** Con los datos obtenidos - proceden encontrar los patrones de la enfermedad **", "\n")
if __name__ == "__main__":
    main()
