function delete_confirmation(id, name) {
    document.getElementById('confirm-delete').style.display = 'unset';
    document.getElementsByClassName('popup-background')[0].classList.add('visible');
    document.getElementById('delete-title').innerText = 'Are you sure you want to delete ' + name + '?';
    document.getElementById('delete-id').setAttribute('value', id);
}

function cancel_delete() {
    document.getElementById('confirm-delete').style.display = 'none';
    document.getElementsByClassName('popup-background')[0].classList.remove('visible');
}