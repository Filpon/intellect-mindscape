import React from 'react';
import { Modal, Button } from 'react-bootstrap';

interface ErrorModalProps {
  show: boolean;
  handleClose: () => void;
  title: string;
  messageBody: string;
  onConfirm: () => void;
}

export const ModalWindowConfirm: React.FC<ErrorModalProps> = ({
  show,
  handleClose,
  title,
  messageBody,
  onConfirm,
}) => {
  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>{messageBody}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Cancel
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          {' '}
          {/* Confirm button */}
          Confirm
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalWindowConfirm;
