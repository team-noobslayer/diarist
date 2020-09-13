const BACKEND_URL = 'http://localhost:5000/diarist';
const NUMBER_OF_MOODS = 4;

if (!sessionStorage.getItem('token')) {
    window.location.replace("index.html");
}

function logout() {
    sessionStorage.removeItem('token');
    window.location.href = "index.html";
}

function getMoods(entry) {
    let output = [];
    moodString = entry.mood.toString(2);
    while (moodString.length < NUMBER_OF_MOODS) {
        moodString = "0" + moodString;
    }
    for (let i = 0; i < moodString.length; i++) {
        output.push(Number(moodString.charAt(i)));
    }
    return output
}

var app = new Vue({
    el: '#app',
    data: {
        username: null,
        journalEntries: []
    },
    methods: {
        getMoods: getMoods
    },
    created: function () {
        axios({
            method: 'get',
            url: BACKEND_URL,
            headers: {
                Authorization: sessionStorage.getItem("token")
            }
        })
        .then((res) => {
            this.journalEntries = res.data.journal_entries;
            this.username = res.data.username;
        })
        .error((err) => console.error(err));
    }
  })