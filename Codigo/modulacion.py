import numpy as np 
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt


'''
Parte 1
'''

# Mensaje digital en bits
bits = np.genfromtxt('bits10k.csv',delimiter=',')

# Frecuencia de operacion de la portadora en Hz
f = 5000 

#Periodo completo en segundos
T = 1/f

# Numero de puntos de muestreo por periodo
pts = 50

# Vector de puntos para cada periodo
tp = np.linspace(0, T, pts)

# Forma de onda de la de la portadora
sin = np.sin(2*np.pi*f*tp)

plt.plot(tp, sin)
plt.title('Forma de onda de la portadora')
plt.ylabel('Amplitud')
plt.xlabel('tiempo(s)')
plt.savefig('../Graficos/portadora.png')
plt.close()

# Frecuencia de muestreo
fm = pts/T

# Vector de puntos para toda la senal TX
t = np.linspace(0, len(bits)*T, len(bits)*pts)

# Inicializar vector para la senal
senal = np.zeros(t.shape) 

# Senal modulada BPSK
for p,b in enumerate(bits):
    if b == 1:
        senal[p*pts:(p+1)*pts] = sin
    else:
        senal[p*pts:(p+1)*pts] = -sin

# Visualizacion de los primeros bits modulados
pb = 10
plt.plot(senal[0:pb*pts])
plt.title('Visualizacion de los primeros 10 bits modulados sin ruido')
plt.ylabel('Amplitud')
plt.xlabel('tiempo(s)')
plt.savefig('../Graficos/senal.png')
plt.close()

'''
Parte 2
'''
# Potencia instantanea
Pi = senal**2

# Potencia promedio
Pp = integrate.trapz(Pi, t)/(len(bits)*T)

print('------------------------------------------------')
print("La potencia promedio es: " + str(Pp))
print('------------------------------------------------')

'''
Parte 3
'''

# Calculo del sigma necesario para cada SNR desde -2 a 3 junto con la potencia del ruido
SNR = [-2,-1,0,1,2,3]
Pr = []
sigma = []

for v in SNR:
    Pr.append(Pp/(10**(v/10)))

for p in Pr:
    sigma.append(np.sqrt(p))

# Ruido a inserta a la senal en el canal
ruido = []
for s in sigma:
    ruido.append(np.random.normal(0, s, senal.shape))

# Simulacion del canal con ruido
Rx = []
for r in ruido:
    Rx.append(senal+r)    

# Visualizacion del canal con ruido
pb = 10
for i,r in enumerate(Rx):
    plt.title('Visualizacion de los primeros 10 bits modulados para un SNR de: '+str(SNR[i]))
    plt.ylabel('Amplitud')
    plt.xlabel('tiempo(s)')
    plt.plot(r[0:pb*pts])
    plt.savefig('../Graficos/Rx'+str(i)+'.png')
    plt.close()

'''
Parte 4
'''
# Grafica de la densidad espectral de potencia antes del canal ruidoso

plt.figure(figsize=(7,5), dpi= 80, facecolor='w', edgecolor='k')
fesp, DEP = signal.welch(senal, fm, nperseg=1024)
plt.semilogy(fesp, DEP)
plt.title('Densidad espectral de potencia sin ruido')
plt.xlabel('frequencia(Hz)')
plt.ylabel('DEP(V^2/Hz)')
plt.savefig('../Graficos/DEP_sin_ruido.png')
plt.grid(axis='y', alpha=0.75)
plt.close()

# Grafica de la densidad espectral de potencia con ruido para los diferentes SNR

for i, r in enumerate(Rx):
    plt.figure(figsize=(7,5), dpi= 80, facecolor='w', edgecolor='k')
    fesp, DEP = signal.welch(r, fm, nperseg=1024)
    plt.semilogy(fesp, DEP)
    plt.title('Densidad espectral de potencia para un SNR de: '+str(SNR[i]))
    plt.xlabel('frequencia(Hz)')
    plt.ylabel('DEP(V^2/Hz)')
    plt.savefig('../Graficos/DEP_con_ruido'+str(i)+'.png')
    plt.grid(axis='y', alpha=0.75)
    plt.close()

'''
Parte 5
'''

# Energia instantanea de la onda portadora
Ei = np.sum(sin**2)

# Contenedor para los bits recibidos
bitsRx = []
for i in range(len(Rx)):
    bitsRx.append(np.zeros(bits.shape))

# Demodulacion de la señal por detección de energía
for i in range(len(Rx)):
    for p,b in enumerate(bits):
        Ep=np.sum(Rx[i][p*pts:(p+1)*pts] * sin)
        if Ep>Ei/2:
            bitsRx[i][p]=1
        else:
            bitsRx[i][p]=0

# Calculo del error para cada SNR
err = []
for brx in bitsRx:
    err.append(np.sum(np.abs(bits - brx)))

# Calculo del Bit Error Rate para cada SNR
BER = []
for e in err:
    BER.append(e/len(bits))
   
print('------------------------------------------------')
print('El numero total de bits es: '+str(len(bits)))
for i in range(len(bitsRx)):
    print('Para SNR = '+str(SNR[i])+' se encontraron: '+str(err[i])+' errores')
    print('El BER es de: '+str(BER[i]))
print('------------------------------------------------')

'''
Parte 5
'''

# Grafico de BER vs SNR
plt.bar(SNR, BER)
plt.title('BER vs SNR')
plt.xlabel('SNR')
plt.ylabel('BER')
plt.savefig('../Graficos/BERvsSNR.png')
plt.close()