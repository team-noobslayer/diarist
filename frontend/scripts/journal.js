const BACKEND_URL = 'http://localhost:5000/diarist'
const NUMBER_OF_MOODS = 4

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
            this.journalEntries = res.data;
        })
        .error((err) => console.error(err))
    }
  })