import FirebaseStoreSingleton from '../Stores/FirebaseStore'

class HarvestedDataController {
    constructor() {
        this.firebaseStore = FirebaseStoreSingleton.getInstance()
    }

    createHarvestedData(data) {
        return this.firebaseStore.setData("data/", data);
    }
}

export default HarvestedDataController