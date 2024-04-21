import React, { useState } from "react";
import Modal from "react-modal";
import "./index.css";
import botLogo from "/public/bot.png";

function PopUpChat() {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const toggleModal = () => {
    setModalIsOpen(!modalIsOpen); // Invertim valoarea pentru a deschide/închide fereastra
  };

  return (
    <div className="popUpContainer">
      <img
        src={botLogo}
        alt="Logo"
        className="bot-logo"
        onClick={toggleModal} // Apelam functia toggleModal atunci cand se apasa pe poza
      />
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={toggleModal} // Inchidem fereastra atunci cand se face click afara de ea
        contentLabel="Chat Modal"
        className="custom-modal-content"
        overlayClassName="custom-modal-overlay"
      >
        <h2>Chat</h2>
        <p>Chatul tău va fi aici...</p>
      </Modal>
    </div>
  );
}

export default PopUpChat;
