window.onload = () => {
    let listItems = document.getElementsByClassName('list-item');

    for (let item of listItems) {
        item.onmouseover = (self) => {
            let actions = self.target.closest('tr').querySelector('.list-actions');
            actions.style.visibility = 'visible';
        }

        item.onmouseout = (self) => {
            let actions = self.target.closest('tr').querySelector('.list-actions');
            actions.style.visibility = 'hidden';
        }
    }
}
