import React from 'react';
import { Modal, Button } from 'react-bootstrap';

interface ErrorModalProps {
  show: boolean;
  handleClose: () => void;
  title: string;
  messageBody: string;
}

export const ModalWindow: React.FC<ErrorModalProps> = ({
  show,
  handleClose,
  title,
  messageBody,
}) => {
  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>{messageBody}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalWindow;
