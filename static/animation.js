function toggleAddSection() {
    const addForm = document.getElementById('add-form');
    addForm.style.display = addForm.style.display === 'none' ? 'block' : 'none';

    const addSentence = document.querySelector('.add_sentence');
    addSentence.style.display = addForm.style.display === 'none' ? 'block' : 'none';

    toggleSentences(addForm);
}

function toggleSearchSection() {
    const searchForm = document.getElementById('search-form');
    searchForm.style.display = searchForm.style.display === 'none' ? 'block' : 'none';

    const searchSentence = document.querySelector('.search_sentence');
    searchSentence.style.display = searchForm.style.display === 'none' ? 'block' : 'none';

    toggleSentences(searchForm);
}

function toggleUpdateSection() {
    const updateForm = document.getElementById('update-form');
    updateForm.style.display = updateForm.style.display === 'none' ? 'block' : 'none';

    const updateSentence = document.querySelector('.update_sentence');
    updateSentence.style.display = updateForm.style.display === 'none' ? 'block' : 'none';

    toggleSentences(updateForm);
}

function toggleDeleteSection() {
    const deleteForm = document.getElementById('delete-form');
    deleteForm.style.display = deleteForm.style.display === 'none' ? 'block' : 'none';

    const deleteAllForm = document.getElementById('delete-all-form');
    deleteAllForm.style.display = deleteAllForm.style.display === 'none' ? 'block' : 'none';

    const deleteSentence = document.querySelector('.delete_sentence');
    deleteSentence.style.display = deleteForm.style.display === 'none' ? 'block' : 'none';

    toggleSentences(deleteForm);
    toggleSentences(deleteAllForm);
}

function toggleSentences(formElement) {
    const sentences = document.querySelectorAll('.sentence');
    sentences.forEach(sentence => {
        sentence.style.display = formElement.style.display === 'none' ? 'block' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const sentences = [
        '<span style="color: #29B60B;">Where</span> Every Event Starts, <span style="color: #29B60B;">GetTogetherGo!</span> ',
        'And a <span style="color: #29B60B;">new beginning</span> unfolds.',
        '<span style="color: #29B60B;">Discover, connect, enjoy!</span>'
    ];

    const textContainer = document.getElementById('lost-item-text');

    let currentSentence = 0;
    let currentChar = 0;
    let addingText = true;

    const updateText = () => {
        textContainer.innerHTML = sentences[currentSentence].substring(0, currentChar);

        if (addingText) {
            if (currentChar === sentences[currentSentence].length) {
                addingText = false;
                setTimeout(updateText, 300);
            } else {
                currentChar++;
                setTimeout(updateText, 40);
            }
        } else {
            if (currentChar === 0) {
                addingText = true;
                currentSentence = (currentSentence + 1) % sentences.length;
                setTimeout(updateText, 300);
            } else {
                currentChar--;
                setTimeout(updateText, 40);
            }
        }
    };

    updateText();
});
