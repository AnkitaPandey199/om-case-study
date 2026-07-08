import { createExampleAction } from './example';
import { createMockActionContext } from '@backstage/plugin-scaffolder-node-test-utils';

describe('createExampleAction', () => {
  it('should create a file', async () => {
    const action = createExampleAction();

    await expect(
      action.handler(
        createMockActionContext({
          input: {
            filename: 'repo.txt',
            contents: 'New Repo File Created by custom action',
          },
        }),
      ),
    ).resolves.toBeUndefined();
  });
});