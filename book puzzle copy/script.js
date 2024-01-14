document.addEventListener('DOMContentLoaded', () => {
    const notes = document.querySelectorAll('.note');

    notes.forEach(note => {
        note.addEventListener('dragstart', handleDragStart);
        note.addEventListener('dragend', handleDragEnd);
    });

    function handleDragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.id);

        // You could add some styling to the note being dragged if you like
        e.target.classList.add('dragging');
    }

    function handleDragEnd(e) {
        const id = e.dataTransfer.getData('text/plain');
        const note = document.getElementById(id);

        // Update the note's position
        note.style.left = (e.clientX - 50) + 'px'; // 50 is half the width of the note for centering
        note.style.top = (e.clientY - 50) + 'px'; // 50 is half the height of the note for centering

        // Remove the additional styling
        note.classList.remove('dragging');
    }
});
