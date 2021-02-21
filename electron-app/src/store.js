const Store = require('electron-store');


const schema = {
    num_calls: {
        type: 'number',
        minimum: 0,
        default: 0
    },
    avg_speak_time: {
        type: 'number',
        default: 0
    },
    avg_pronounciation_score: {
        type: 'number',
        default: 0
    },
    avg_num_pauses: {
        type: 'number',
        default: 0
    },
    avg_rate_of_speech: {
        type: 'number',
        default: 0,
    }
};

const store = new Store({ schema });

module.exports = store;