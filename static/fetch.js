async function updatePerson() {
    const formData = new FormData(document.getElementById('update-form'));
    const id = formData.get('id');

    try {
        const response = await fetch(`/update/${id}`, {
            method: 'PATCH',
            body: formData,
        });

        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Failed to update person:', response.statusText);
        }
    } catch (error) {
        console.error('Error updating person:', error);
    }
}


async function deletePerson() {
    const formData = new FormData(document.getElementById('delete-form'));
    const id = formData.get('delete');

    try {
        const response = await fetch(`/delete/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Failed to delete person:', response.statusText);
        }
    } catch (error) {
        console.error('Error deleting person:', error);
    }
}


    async function deleteAllPersons() {
        try {
            const response = await fetch('/delete-all', {
                method: 'DELETE'
            });

            if (response.ok) {
                window.location.reload(); 
            } else {
                console.error('Failed to delete all persons:', response.statusText);
            }
        } catch (error) {
            console.error('Error deleting all persons:', error);
        }
    }

