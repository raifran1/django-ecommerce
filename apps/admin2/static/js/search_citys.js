function populateUf() {
	const ufSelect = document.querySelector('#uf')
	const url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/'
	fetch(url)
	.then(res => res.json())
	.then(states => {
		for (const state of states) {
			ufSelect.innerHTML +=  `<option value="${state.id}">${state.nome}</option>`
		}
	})
}

populateUf();

function getCites(event) {
	const citiesSelect = document.querySelector('#city')
	console.log(event.target.value)

	citiesSelect.innerHTML = "<option selected>Selecione sua Cidade</option>"
	citiesSelect.disabled = true

	const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${event.target.value}/municipios/`
	fetch(url)
	.then(res => res.json())
	.then(cities => {
		for (const city of cities) {
			citiesSelect.innerHTML +=  `<option value="${city.id}">${city.nome}</option>`
		}

		citiesSelect.disabled = false
	})
}

document
	.querySelector('#uf')
		.addEventListener('change', getCites)