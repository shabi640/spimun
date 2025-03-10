import mitt from 'mitt';

type Events = {
  'login': any;
  'logout': any;
};

const emitter = mitt<Events>();

export default emitter; 