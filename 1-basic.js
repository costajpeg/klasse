

// Objeto dados

let dados = { // ex 18
    nome: "Maria Antonia",
    idade: 25,
    notas: [8, 9, 10],
    cidades: ["POA", "RJ"],
    salario: 2500
};
//objetos podem conter arrays, e a função deve retornar um novo objeto contendo apenas as chaves que possuem arrays como valor. No exemplo acima, o resultado seria:

function pegarArrays(objeto) {

    let novoObjeto = {};

    for (let chave in objeto) {

        if (Array.isArray(objeto[chave])) {
            novoObjeto[chave] = objeto[chave];
        }
    }

    return novoObjeto;
}

console.log(pegarArrays(dados));
