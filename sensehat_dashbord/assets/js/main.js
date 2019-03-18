config = {
  "apiKey": "AIzaSyBYCO3HevrkCz38GZHpdH7JShA17Kd39B4",
  "authDomain": "iotlabo5.firebaseapp.com",
  "databaseURL": "https://iotlabo5.firebaseio.com",
  "projectId": "iotlabo5",
  "storageBucket": "iotlabo5.appspot.com",
  "messagingSenderId": "7052501175"
}
firebase.initializeApp(config)

const container = document.getElementById('contentTable');
const submitbutton = document.getElementById('submit');

firebase.database().ref('environment').on('value', (snapshot) => {
	container.innerHTML = ''
	const titles = snapshot.val()
	const keys = Object.keys(titles)
	const values = Object.values(titles)
	console.log(keys)
	console.log(values)
	for(i=0; i < 3; i++){
		container.innerHTML += '<tr><td>' + keys[i] + '</td><td>' +  values[i].value  + '</td><td>' +  values[i].unit  + '</td></tr><br>'
	}
});


submitbutton.addEventListener('click', (e) => {
	e.preventDefault()
	const color = document.getElementById('colorField').value;
		document.getElementById('colorBox').style.background = color
	firebase.database().ref('ambilight').set(color);
})

