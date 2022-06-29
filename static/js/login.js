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


