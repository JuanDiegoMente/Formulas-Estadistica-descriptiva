# Voy a ser mejor que el que esta escribiendo esto
import math


def sumatorio(ar):
	suma = 0
	for i in range(len(ar)):
		suma += ar[i]
	return suma


class FormulasCompartidas:

	# Frecuencia absoluta acumulada
	def obtener_Fi(self, ar):
		acumulado = [0]
		for i in range(len(ar)):
			acumulado.append(acumulado[i] + ar[i])
		return acumulado[1:]


	# Frecuencia relativa
	def obtener_hi(self, fi, n):
		return [round(fi[j] / n, 2) for j in range(len(fi))]


	# Media
	def obtener_media(self, fi, xi, n):
		multiplicar = [fi[i] * xi[i] for i in range(len(xi))]
		return sumatorio(multiplicar) / n


	# Rango
	def obtener_rango(self, xi):
		return max(xi) - min(xi)


	# Desviacion media
	def obtener_DM(self, fi, xi, n, media):
		xi_menos_x_por_fi = [abs(xi[n] - media) * fi[n] for n in range(len(xi))]
		return sumatorio(xi_menos_x_por_fi) / n


	# Varianza
	def obtener_varianza(self, fi, xi, n, media):
		xi2_menos_fi = [xi[h] ** 2 * fi[h] for h in range(len(fi))]
		return (sumatorio(xi2_menos_fi) / n) - media ** 2


	# Desviacion tipica
	def obtener_desviacion_tipica(self, var):
		return math.sqrt(var)


	# Coeficiente de variacion
	def obtener_coeficiente_variacion(self, media, desvT):
		return desvT / media




class DatosSimples(FormulasCompartidas):

	# Moda
	def obtener_moda(self, fi, xi):
		maxD = max(fi)
		indice = fi.index(maxD)
		return xi[indice]


	# Mediana
	def obtener_mediana(self, arr):
		copia = arr.sort(reverse = True)
		if len(arr) % 2 == 0:
			indice = len(arr)/2
			subIndice = (copia[indice] + copia[indice + 1]) / 2
			return arr[subIndice]

		else:
			subIndice = (copia[len(copia)] + 1) / 2
			return arr[subIndice]


	# Cuartiles, deciles o percentiles
	def parametros_posicion(xi, n, Fi, cdp, k):
		# cdp => Cuartil (4), Decil (10), Percentil (100)
		# k => Clase
		k_x_n = k*n/cdp

		if k_x_n in Fi:
			indice = Fi.index(k_x_n)
			return (xi[indice] + xi[indice + 1]) / 2

		else:
			for j in range(len(xi)):
				if Fi[j] > k_x_n:
					indice = Fi.index(Fi[j])
					return xi[indice]



class DatosAgrupados(FormulasCompartidas):

	# Sacar x sub i
	def get_xi_Intervalos(self, intervalo):
		var = []
		for i in range(len(intervalo)):
			x = intervalo[i][0] + intervalo[i][1]
			var.append( x/2 )
		return var


	# Meidana
	def get_mediana_Intervalos(self, fi, intervalos, n, Fi):
		'Li + ((n/2 - F(i-1))/fi) * amp'
		n_sobre_2 = int(n/2)
		# Si n/2 esta en Me = Ls
		if n_sobre_2 in Fi:
			indice = Fi.index(n_sobre_2)
			return intervalos[indice][1]

		# Si no esta aplicamos esto la formula de la doc de esta funcion
		else:
			# Ahora hay que sacar el indice, el cual sera el primer valor de la Fi
			# que supere a n/2
			indice = 0
			for i in range(len(fi)):
				if Fi[i] > n_sobre_2:
					indice = Fi.index(Fi[i])
					break

			# amp = inter[x] - inter[y] => >= 1
			amp = intervalos[indice][1] - intervalos[indice][0]

			# (n/2 - F(i-1)) / fi
			parteCentral = (n_sobre_2 - Fi[indice-1])/fi[indice]
			return intervalos[indice][0] + parteCentral * amp


	# Moda
	def get_moda_Intervalos(self, fi, intervalos):
		maxV = max(fi) # -> Dato con mayor frecuencia abs.
		indice = fi.index(maxV) # -> Nos da la fila donde estan los datos que usaremos
		amp = intervalos[indice][1] - intervalos[indice][0]

		# fi - f(i-1)
		parteArriba = fi[indice] - fi[indice-1]

		# parteArriba + (fi - f(i+1))
		parteAbajo = parteArriba + fi[indice] - fi[indice+1]

		return intervalos[indice][0] + (parteArriba/parteAbajo) * amp


	# Deciles, percentiles o cuartiles
	def parametros_posicion_Intervalos(self, cdp, n, k, intervalos, Fi):

		kn_cdp = (k*n)/cdp
		if kn_cdp in Fi:
			indice = Fi.index(kn_cdp)
			return intervalos[indice][1]

		else:
			indice = 0
			for i in range(len(Fi)):
				if Fi[i] > kn_cdp:
					indice = Fi.index(Fi[i])
					break

			amp = intervalos[indice][1] - intervalos[indice][0]

			# kn_cdp - F(i-1)
			parteArriba = kn_cdp - Fi[indice-1]

			# Fi - F(i-1)
			parteAbajo = Fi[indice] - Fi[indice-1]

			return intervalos[indice][0] + (parteArriba/parteAbajo) * amp



