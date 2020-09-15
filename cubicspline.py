# TFY4104/4107/4115 Fysikk høsten 2020.
#
# Programmet bestemmer høyden til de 8 festepunktene ved å trekke
# tilfeldige heltall mellom 50 og 300 (mm). Når festepunktene er
# akseptable, beregnes baneformen med mm som enhet. 
# Etter dette regnes høydeverdiene om til meter som enhet.
# Hele banens form y(x) beregnes
# ved hjelp av 7 ulike tredjegradspolynomer, på en slik måte
# at både banen y, dens stigningstall dy/dx og dens andrederiverte
# d2y/dx2 er kontinuerlige i alle 6 indre festepunkter.
# I tillegg velges null krumning (andrederivert) 
# i banens to ytterste festepunkter (med bc_type='natural' nedenfor).
# Dette gir i alt 28 ligninger som fastlegger de 28 koeffisientene
# i de i alt 7 tredjegradspolynomene.

# Programmet aksepterer de 8 festepunktene først når
# følgende betingelser er oppfylt:
#
# 1. Starthøyden er stor nok og en del høyere enn i de øvrige 7 festepunktene.
# 2. Helningsvinkelen i startposisjonen er ikke for liten.
# 3. Banens maksimale helningsvinkel er ikke for stor.
#
# Med disse betingelsene oppfylt vil 
# (1) objektet (kula/skiva/ringen) fullføre hele banen selv om det taper noe 
#     mekanisk energi underveis;
# (2) objektet få en fin start, uten å bruke for lang tid i nærheten av
#     startposisjonen; 
# (3) objektet forhåpentlig rulle rent, uten å gli/slure.

# Vi importerer nødvendige biblioteker:
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

# Horisontal avstand mellom festepunktene er 200 mm
h = 200
xfast=np.asarray([0,h,2*h,3*h,4*h,5*h,6*h,7*h])
# Vi begrenser starthøyden (og samtidig den maksimale høyden) til
# å ligge mellom 250 og 300 mm
# ymax = 300
# # yfast: tabell med 8 heltall mellom 50 og 300 (mm); representerer
# # høyden i de 8 festepunktene
# yfast=np.asarray(np.random.randint(50, ymax, size=8))
# # inttan: tabell med 7 verdier for (yfast[n+1]-yfast[n])/h (n=0..7); dvs
# # banens stigningstall beregnet med utgangspunkt i de 8 festepunktene.
# inttan = np.diff(yfast)/h
# attempts=1
# while-løkken sjekker om en eller flere av de 3 betingelsene ovenfor
# ikke er tilfredsstilt; i så fall velges nye festepunkter inntil
# de 3 betingelsene er oppfylt
# while (yfast[0] < yfast[1]*1.04 or
#        yfast[0] < yfast[2]*1.08 or
#        yfast[0] < yfast[3]*1.12 or
#        yfast[0] < yfast[4]*1.16 or
#        yfast[0] < yfast[5]*1.20 or
#        yfast[0] < yfast[6]*1.24 or
#        yfast[0] < yfast[7]*1.28 or
#        yfast[0] < 250 or
#        np.max(np.abs(inttan)) > 0.4 or
#        inttan[0] > -0.2):
#           yfast=np.asarray(np.random.randint(0, ymax, size=8))
#           inttan = np.diff(yfast)/h
#           attempts=attempts+1

# Når programmet her har avsluttet while-løkka, betyr det at
# tallverdiene i tabellen yfast vil resultere i en tilfredsstillende bane. 

# Omregning fra mm til m:
xfast = xfast/1000
yfast = np.asarray([0.255,0.183,0.189,0.188,0.129,0.091,0.151,0.171])

#Programmet beregner deretter de 7 tredjegradspolynomene, et
#for hvert intervall mellom to nabofestepunkter.

#Med scipy.interpolate-funksjonen CubicSpline:
cs = CubicSpline(xfast, yfast, bc_type='natural')
xmin = 0.000
xmax = 1.401
dx = 0.001
x = np.arange(xmin, xmax, dx)
Nx = len(x)
y = cs(x)
dy = cs(x,1)
d2y = cs(x,2)
g = 9.81
y0 = 0.255
c_kule = 2/5
mass = 1
beta_rad = np.arctan(dy)
beta_deg = 180*beta_rad/np.pi
v = np.sqrt((2*g*(y0 - y)/(1+c_kule)))
curl = d2y/pow((1+pow(dy,2)),3/2)
a_perp = v*v*curl
acc = -g*np.sin(beta_rad)/(1+c_kule)

N = mass*(g*np.cos(beta_rad) + a_perp)
#Plotting

baneform = plt.figure('y(x)',figsize=(12,3))
plt.plot(x,y,xfast,yfast,'*')
plt.title('Banens form')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$y(x)$ (m)',fontsize=20)
plt.ylim(0,0.350)
plt.grid()
#baneform.savefig("baneform.pdf", bbox_inches='tight')
#baneform.savefig("baneform.png", bbox_inches='tight')

baneform = plt.figure('$\kappa$(x)',figsize=(12,3))
plt.plot(x,curl)
plt.title('Krumning')
plt.xlabel('$x$ (m)',fontsize=20)
plt.ylabel('$\kappa$(x) (1/m)',fontsize=20)
# plt.ylim(0,0.350)
plt.grid()
# plt.show()

# print('Antall forsøk',attempts)
print('Festepunkthøyder (m)',yfast)
print('Banens høyeste punkt (m)',np.max(y))

print('NB: SKRIV NED festepunkthøydene når du/dere er fornøyd med banen.')
print('Eller kjør programmet på nytt inntil en attraktiv baneform vises.')

graf_beta = plt.figure('B(x)',figsize=(12,3))
plt.grid()
plt.title('Beta')
plt.xlabel('x (m)')
plt.ylabel('\u03b2 (deg)')
plt.plot(x, beta_deg)

graf_v = plt.figure('v(x)',figsize=(12,3))
plt.grid()
plt.plot(x,v)

graf_a_perp = plt.figure('a_perp(x)',figsize=(12,3))
plt.grid()
plt.title('Centripetal acceleration')
plt.xlabel('x (m)')
plt.ylabel('A_perp (ms^-2)')
plt.plot(x,a_perp)

graf_acc = plt.figure('acc(x)',figsize=(12,3))
plt.grid()
plt.title('Acceleration')
plt.xlabel('x (m)')
plt.ylabel('Acceleration (ms^-2)')
plt.plot(x,acc)

normal_force = plt.figure('N(x)', figsize=(12,3))
plt.grid()
plt.plot(x,N)

v_x = v*np.cos(beta_rad)
v_x_avg = np.zeros(len(v_x))
v_x_avg[0] = v_x[0]
dt = np.zeros(len(v_x))

graf_v_x = plt.figure('v_x',figsize=(12,3))
plt.grid()
plt.title('Velocity in x-direction')
plt.plot(x,v_x)

for i in range(1,len(v_x)):
    v_x_avg[i] = 0.5*(v_x[i-1] + v_x[i])
    dt[i] = dx/v_x_avg[i]
    
graf_v_x_avg = plt.figure('v_x_avg',figsize=(12,3))
plt.grid()
plt.title('Average velocity in x-direction')
plt.plot(x,v_x_avg)


print(dt)




