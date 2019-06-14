import Firebase from "firebase";

const firebaseConfig = {
    apiKey: "AIzaSyBo2hYbi41Sm0nEAwNI0gtRw_cbCAE-0-Q",
    authDomain: "datasetwebharvester.firebaseapp.com",
    databaseURL: "https://datasetwebharvester.firebaseio.com",
    projectId: "datasetwebharvester",
    storageBucket: "datasetwebharvester.appspot.com",
    messagingSenderId: "1019301701067",
    appId: "1:1019301701067:web:f1ba32d60d9e01d5"
};

var FirebaseStoreSingleton = (function () {
    var instance;
    
    function createInstance() {
        const firebaseStore = new FirebaseStore();
        return firebaseStore;
    }
    
    return {
        getInstance: function () {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();

class FirebaseStore {
    constructor() {
        this.initFirebase();
    }

    initFirebase() {
        Firebase.initializeApp(firebaseConfig)
        this.db = Firebase.database();
    }

    setData(path, data) {
        this.db.ref(path).push(data);
        return data;
    }

    getData(path) {
        const docRef = this.db.ref(path);
        return docRef.once('value');
    }

    updateData(path, data) {
        const docRef = this.db.ref(path);
        docRef.update(data);
    }
}

export default FirebaseStoreSingleton