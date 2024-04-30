let btn = document.querySelector('button')
let review = document.querySelector('textarea')
let container = document.querySelector('div.container')
let p = document.createElement('p')
p.setAttribute('id', 'sentiment')
container.append(p)

let err_p = document.createElement('p')
err_p.setAttribute('id', 'err')

async function getSentiment(text) {
    let sentiment = await fetch("/", {
        method: 'POST',
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({ text })
    })
    return sentiment.json()
}


btn.addEventListener("click", async () => {
    let text = review.value;
    if (text.trim().length > 0) {
        try {
            err_p.remove()
        } catch (err) { }
        btn.innerHTML = 'Loading...'
        let sentiment = await getSentiment(text)
        btn.innerHTML = 'Submit <i class="fa-solid fa-angle-right"></i>'
        if (sentiment === 'Negative')
            p.innerHTML = `Predicted sentiment: <span id='neg' class='sentiment_span'>${sentiment}</span>`
        else
            p.innerHTML = `Predicted sentiment: <span id='pos' class='sentiment_span'>${sentiment}</span>`
    } else {
        container.append(err_p)
        err_p.innerText = 'Please enter something !'
    }
})