setTimeout(() => {
    const alertElems = document.querySelectorAll('#dj-messages .alert')
    alertElems.forEach((element) => {
        bootstrap.Alert.getOrCreateInstance(element).close()
    })
}, 5000)
