import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import { resolveSafeChildPath } from '@backstage/backend-plugin-api';
import fs from 'fs-extra';

export function createExampleAction() {
  return createTemplateAction({
    id: 'my:custom:action',
    description: 'Creates a file in the temporary workspace',

    schema: {
      input: {},
    },

    async handler(ctx) {
      const filePath = resolveSafeChildPath(
        ctx.workspacePath,
        "workspace/repo.txt",
      );

      await fs.outputFile(
        filePath,
        'New Repo File Created by custom action',
      );

      ctx.logger.info(`Created ${filePath}`);
    },
  });
}