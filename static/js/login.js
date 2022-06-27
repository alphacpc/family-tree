let formLogin = document?.querySelector(".divLogin form")
let divMessageError = document?.querySelector(".divMessageError")


let funcShowMessage = (message) => {
    let p = document.createElement('p')
    p.innerText = message
    divMessageError.append(p)
    divMessageError.classList.add('show')

    setTimeout(() => {
        console.log("first")
        p.innerText = ''
        p.remove()
        divMessageError.classList.remove('show')

    }, 3000)
}




formLogin.addEventListener('submit', async(e) => {
    e.preventDefault()

    let email = e.target['email'].value.trim()
    let mdp = e.target['mdp'].value.trim()

    if( email == "" || mdp == "" ){
        funcShowMessage("Veillez remplir tous les champs")
    }
    else if (mdp.length < 2){
        funcShowMessage("Veillez donner un mot de passe contenant au moins 8 caractères !")
    }
    else{
        let response = await fetch('http://localhost:5000/api/login/',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email, mdp})
        })

        // Récupper les données de l'APIs
        let data = await response.json()

        console.log("Tester le truc")
        if(!data['type']) funcShowMessage(data['message'])
        
    }

})


