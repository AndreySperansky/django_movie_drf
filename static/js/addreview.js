function addReview(name, id) {
    document.getElemetById("contactcomment").value = id;
    document.getElemetById("contactcomment").innerText = `${name}, `
 }