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
    print("Configurando el contexto de cifrado...")
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

    print("Contexto de cifrado configurado.")

    # Datos de pacientes del hospital 1 y 2
    hospital_1_data = [110, 105, 120]
    hospital_2_data = [130, 115, 100]

    print("Cifrando datos de pacientes...")
    # Convertir datos a tensores y cifrarlos
    hospital_1_encrypted = ts.ckks_vector(context, hospital_1_data)
    hospital_2_encrypted = ts.ckks_vector(context, hospital_2_data)

    # Sumar los datos cifrados
    print("Sumando datos cifrados...")
    sum_encrypted = hospital_1_encrypted + hospital_2_encrypted

    # Descifrar la suma
    sum_decrypted = sum_encrypted.decrypt()
    print("Suma de niveles de glucosa:", sum_decrypted)

    # Número total de pacientes
    total_patients = len(hospital_1_data) + len(hospital_2_data)

    # Calcular promedio cifrado
    average_encrypted = sum_encrypted * (1 / total_patients)

    # Descifrar el promedio
    average_decrypted = average_encrypted.decrypt()
    print("Promedio de niveles de glucosa:", average_decrypted)

if __name__ == "__main__":
    main()
