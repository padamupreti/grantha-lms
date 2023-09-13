setTimeout(() => {
    const alertElems = document.querySelectorAll('.alert')
    alertElems.forEach((element) => {
        bootstrap.Alert.getOrCreateInstance(element).close()
    })
}, 3000)
