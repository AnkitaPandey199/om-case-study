import { resolveSafeChildPath } from '@backstage/backend-plugin-api';
import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import fs from 'fs-extra';
//import {z} from 'zod';

export const createNewFileAction = () => {
  return createTemplateAction({
    id: 'my:custom:action',
    description: 'Create an Acme file.',
    schema: {
      input: {
        contents: z => z.string({ description: 'The contents of the file' }),
        filename: z =>
          z.string({
            description: 'The filename of the file that will be created',
          }),
      },
    },

    async handler(ctx) {
      await fs.outputFile(
        resolveSafeChildPath(ctx.workspacePath, ctx.input.filename),
        ctx.input.contents,
      );
    },
  });
};