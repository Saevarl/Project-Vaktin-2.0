import GPUList from '../components/GPUList';

const GPUsPage: React.FC = () => {
  return (
    <div className="w-full h-full overflow-auto">
      <div className="max-w-screen-2xl mx-auto px-4 py-8">
        <GPUList />
      </div>
    </div>
  );
};

export default GPUsPage;