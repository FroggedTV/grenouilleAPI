import logging
import os
import json

from flask import request, jsonify

from helpers.general import safe_json_loads
from helpers.endpoint import secure
from helpers.obs import send_command_to_obs
from models import User

def build_api_stream_system(app):
    """Factory to setup the routes for the stream system api."""

    @app.route('/api/obs/scene/list', methods=['GET'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def get_obs_scene_list(auth_token):
        """
        @api {get} /api/obs/scene/list OBSSceneList
        @apiVersion 1.1.0
        @apiName OBSSceneList
        @apiGroup StreamSystem
        @apiDescription List the available scenes in OBS.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.
        @apiSuccess {String[]} scenes All available scenes with their name as Strings.
        @apiSuccess {String} active_scene Active scene.
        """
        scenes = []
        try:
            result = send_command_to_obs('GetSceneList', {})
            for scene in result['scenes']:
                scenes.append(scene['name'])
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {
                                'scenes': scenes,
                                'active_scene': result['current-scene']
                            }}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/obs/scene/update', methods=['POST'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def post_obs_scene_update(auth_token):
        """
        @api {post} /api/obs/scene/update OBSSceneUpdate
        @apiVersion 1.1.0
        @apiName OBSSceneUpdate
        @apiGroup StreamSystem
        @apiDescription Change the OBS active scene to a new one.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.

        @apiParam {String} scene Name of the scene to change to.
        @apiError (Errors){String} SceneParameterMissing Scene is not present in the parameters.
        @apiError (Errors){String} SceneParameterInvalid Scene is not valid String.
        @apiError (Errors){String} SceneDoesNotExist Specified scene does not exist in OBS.
        """
        data = request.get_json(force=True)

        # scene checks
        scene = data.get('scene', None)
        if scene is None:
            return jsonify({'success': 'no',
                            'error': 'SceneParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(scene, str) or len(scene) == 0:
            return jsonify({'success': 'no',
                            'error': 'SceneParameterInvalid',
                            'payload': {}
                            }), 200

        # Send command to obs
        try:
            result = send_command_to_obs('SetCurrentScene', {'scene-name': scene})
            if ('status' in result
                    and result['status'] == 'error'
                    and result['error'] == 'requested scene does not exist'):
                return jsonify({'success': 'no',
                                'error': 'SceneDoesNotExist',
                                'payload': {}}), 200
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/obs/record/start', methods=['POST'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def post_obs_record_start(auth_token):
        """
        @api {post} /api/obs/record/start OBSRecordStart
        @apiVersion 1.1.0
        @apiName OBSRecordStart
        @apiGroup StreamSystem
        @apiDescription Start the recording by OBS.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.
        @apiError (Errors){String} OBSAlreadyRecording OBS is already recording.
        """
        try:
            result = send_command_to_obs('StartRecording', {})
            if ('status' in result
                    and result['status'] == 'error'
                    and result['error'] == 'recording already active'):
                return jsonify({'success': 'no',
                                'error': 'OBSAlreadyRecording',
                                'payload': {}}), 200
            return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/obs/record/stop', methods=['POST'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def post_obs_record_stop(auth_token):
        """
        @api {post} /api/obs/record/stop OBSRecordStop
        @apiVersion 1.1.0
        @apiName OBSRecordStop
        @apiGroup StreamSystem
        @apiDescription Stop the recording by OBS.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.
        @apiError (Errors){String} OBSNotRecording OBS is not currently recording.
        """
        try:
            result = send_command_to_obs('StopRecording', {})
            if ('status' in result
                    and result['status'] == 'error'
                    and result['error'] == 'recording not active'):
                return jsonify({'success': 'no',
                                'error': 'OBSNotRecording',
                                'payload': {}}), 200
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200


    @app.route('/api/obs/stream/start', methods=['POST'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def post_obs_stream_start(auth_token):
        """
        @api {post} /api/obs/stream/start OBSStreamStart
        @apiVersion 1.1.0
        @apiName OBSStreamStart
        @apiGroup StreamSystem
        @apiDescription Start the streaming by OBS.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.
        @apiError (Errors){String} OBSAlreadyStreaming OBS already streaming to endpoint.
        """
        try:
            result = send_command_to_obs('StartStreaming', {})
            if ('status' in result
                    and result['status'] == 'error'
                    and result['error'] == 'streaming already active'):
                return jsonify({'success': 'no',
                                'error': 'OBSAlreadyStreaming',
                                'payload': {}}), 200
            return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/obs/stream/stop', methods=['POST'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def post_obs_stream_stop(auth_token):
        """
        @api {post} /api/obs/stream/stop OBSStreamStop
        @apiVersion 1.1.0
        @apiName OBSStreamStop
        @apiGroup StreamSystem
        @apiDescription Stop the streaming by OBS.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.
        @apiError (Errors){String} OBSNotStreaming OBS is not currently streaming.
        """
        try:
            result = send_command_to_obs('StopStreaming', {})
            if ('status' in result
                    and result['status'] == 'error'
                    and result['error'] == 'streaming not active'):
                return jsonify({'success': 'no',
                                'error': 'OBSNotStreaming',
                                'payload': {}}), 200
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/obs/status', methods=['GET'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def get_obs_status(auth_token):
        """
        @api {get} /api/obs/status OBSStatus
        @apiVersion 1.1.0
        @apiName OBSStatus
        @apiGroup StreamSystem
        @apiDescription Get OBS streaming and recording status.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.
        @apiSuccess {Boolean} recording Status of the OBS record.
        @apiSuccess {Boolean} streaming Status of the OBS stream.
        """
        try:
            result = send_command_to_obs('GetStreamingStatus', {})
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {
                                'recording': result['recording'],
                                'streaming': result['streaming']
                            }}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/vod/disk_usage', methods=['GET'])
    @secure(app, ['key', 'user'], ['vod_manage'])
    def get_vod_disk_usage(auth_token):
        """
        @api {get} /api/vod/disk_usage VODDiskUsage
        @apiVersion 1.1.0
        @apiName VODDiskUsage
        @apiGroup StreamSystem
        @apiDescription Get the disk usage of all the VOD directory.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiSuccess {Integer} size Size of the root directory in octets.
        @apiError (Errors){String} FileSystemError Internal error manipulating the filesystem.
        """
        try:
            disk_usage = 0
            for root, dirs, files in os.walk(app.config['VOD_PATH']):
                for file in files:
                    disk_usage += os.path.getsize(os.path.join(root, file))
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {
                                'size': disk_usage
                            }}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'FileSystemError',
                            'payload': {}}), 200

    @app.route('/api/vod/file/list', methods=['GET'])
    @secure(app, ['key', 'user'], ['vod_manage'])
    def get_vod_list(auth_token):
        """
        @api {get} /api/vod/file/list VODFileList
        @apiVersion 1.1.0
        @apiName VODFileList
        @apiGroup StreamSystem
        @apiDescription List all VOD files, omitting VOD_PATH root.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} FileSystemError Internal error manipulating the filesystem.

        @apiSuccess {Object[]} entry List of all VOD directories and files.
        @apiSuccess {String} entry.name Name of the entry.
        @apiSuccess {String=dir,file} entry.type Type of the entry.
        @apiSuccess {Integer} entry.size Size of the entry if type is 'file', in octets.
        """
        try:
            vod_files = []
            for root, dirs, files in os.walk(app.config['VOD_PATH']):
                for dir in dirs:
                    vod_files.append({
                        'filename': os.path.join(root, dir)[len(app.config['VOD_PATH'])+1:],
                        'type': 'dir'
                    })
                for file in files:
                    vod_files.append({
                        'filename': os.path.join(root, file)[len(app.config['VOD_PATH'])+1:],
                        'type': 'file',
                        'size': os.path.getsize(os.path.join(root, file))
                    })
            return jsonify({'success': 'yes',
                        'error': '',
                        'payload': {
                            'vod': vod_files
                        }}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                        'error': 'FileSystemError',
                        'payload': {}}), 200


    @app.route('/api/vod/file/delete', methods=['POST'])
    @secure(app, ['key', 'user'], ['vod_manage'])
    def post_vod_file_delete(auth_token):
        """
        @api {post} /api/vod/file/delete VODFileDelete
        @apiVersion 1.1.0
        @apiName VODFileDelete
        @apiGroup StreamSystem
        @apiDescription Delete a VOD file or directory.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} FileSystemError Internal error manipulating the filesystem.

        @apiParam {String} filename Path of the file to delete (equal to what vod_file_list returns).
        @apiError (Errors){String} FilenameParameterMissing Filename is not present in the parameters.
        @apiError (Errors){String} FilenameParameterInvalid Filename is not valid String.
        @apiError (Errors){String} VODFileDoesntExist There is no VOD file or directory with the specified filename.
        @apiError (Errors){String} VODDirectoryNotEmpty Impossible to remove a directory not empty.
        """
        data = request.get_json(force=True)

        # filename checks
        filename = data.get('filename', None)
        if filename is None:
            return jsonify({'success': 'no',
                            'error': 'FilenameParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(filename, str) or len(filename) == 0:
            return jsonify({'success': 'no',
                            'error': 'FilenameParameterInvalid',
                            'payload': {}
                            }), 200

        try:
            # Check if path is valid and delete
            path = os.path.join(app.config['VOD_PATH'], filename)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                try:
                    os.rmdir(path)
                except OSError as e:
                    return jsonify({'success': 'no',
                                'error': 'VODDirectoryNotEmpty',
                                'payload': {}
                                }), 200
            else:
                return jsonify({'success': 'no',
                                'error': 'VODFileDoesntExist',
                                'payload': {}
                                }), 200

            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                        'error': 'FileSystemError',
                        'payload': {}}), 200

    @app.route('/api/vod/dir/create', methods=['POST'])
    @secure(app, ['key', 'user'], ['vod_manage'])
    def post_vod_dir_create(auth_token):
        """
        @api {post} /api/vod/dir/create VODDirCreate
        @apiVersion 1.1.0
        @apiName VODDirCreate
        @apiGroup StreamSystem
        @apiDescription Create a directory for VOD.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} FileSystemError Internal error manipulating the filesystem.

        @apiParam {String} dir Path of the dir to create, without any "." character. "/" are accepted for sub directories.
        @apiError (Errors){String} DirParameterMissing dir is not present in the parameters.
        @apiError (Errors){String} DirParameterInvalid dir is not valid String.
        @apiError (Errors){String} DirAlreadyExists There is no VOD file or directory with the specified filename.
        """
        data = request.get_json(force=True)

        # filename checks
        dir = data.get('dir', None)
        if dir is None:
            return jsonify({'success': 'no',
                            'error': 'DirParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(dir, str) or len(dir) == 0 or '.' in dir:
            return jsonify({'success': 'no',
                            'error': 'DirParameterInvalid',
                            'payload': {}
                            }), 200

        try:
            # Check if path exists
            path = os.path.join(app.config['VOD_PATH'], dir)
            if os.path.isdir(path):
                return jsonify({'success': 'no',
                                'error': 'DirAlreadyExists',
                                'payload': {}
                                }), 200
            os.makedirs(path, exist_ok=True)
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                        'error': 'FileSystemError',
                        'payload': {}}), 200

    @app.route('/api/vod/file/move', methods=['POST'])
    @secure(app, ['key', 'user'], ['vod_manage'])
    def post_vod_file_move(auth_token):
        """
        @api {post} /api/vod/file/move VODFileMove
        @apiVersion 1.1.0
        @apiName VODFileMove
        @apiGroup StreamSystem
        @apiDescription Move a VOD file.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} FileSystemError Internal error manipulating the filesystem.

        @apiParam {String} source Path of the file to move (equal to what vod_file_list returns).
        @apiError (Errors){String} SourceParameterMissing Source is not present in the parameters.
        @apiError (Errors){String} SourceParameterInvalid Source is not valid String.
        @apiError (Errors){String} SourceFileDoesntExist There is no VOD file with the specified source path.

        @apiParam {String} destination Path where to move the file.
        @apiError (Errors){String} DestinationParameterMissing Destination is not present in the parameters.
        @apiError (Errors){String} DestinationParameterInvalid Destination is not a valid String.
        @apiError (Errors){String} DestinationFileAlreadyExist There is already a file with such path.
        @apiError (Errors){String} DestinationRootDirectoryMissing Destination path has no root directory created yet.
        """
        data = request.get_json(force=True)

        # source checks
        source = data.get('source', None)
        if source is None:
            return jsonify({'success': 'no',
                            'error': 'SourceParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(source, str) or len(source) == 0:
            return jsonify({'success': 'no',
                            'error': 'SourceParameterInvalid',
                            'payload': {}
                            }), 200

        # output checks
        destination = data.get('destination', None)
        if destination is None:
            return jsonify({'success': 'no',
                            'error': 'DestinationParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(destination, str) or len(destination) == 0:
            return jsonify({'success': 'no',
                            'error': 'DestinationParameterInvalid',
                            'payload': {}
                            }), 200

        try:
            # Check if path are valids
            path_source = os.path.join(app.config['VOD_PATH'], source)
            path_destination = os.path.join(app.config['VOD_PATH'], destination)
            if not os.path.isfile(path_source):
                return jsonify({'success': 'no',
                                'error': 'SourceFileDoesntExist',
                                'payload': {}
                                }), 200
            if os.path.isfile(path_destination) or os.path.isdir(path_destination):
                return jsonify({'success': 'no',
                                'error': 'DestinationFileAlreadyExist',
                                'payload': {}
                                }), 200

            path_root = os.path.abspath(os.path.join(app.config['VOD_PATH'], destination, os.pardir))
            logging.error(path_root)
            if not os.path.isdir(path_root):
                return jsonify({'success': 'no',
                                'error': 'DestinationRootDirectoryMissing',
                                'payload': {}
                                }), 200
            os.rename(path_source, path_destination)
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {}}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                        'error': 'FileSystemError',
                        'payload': {}}), 200

    @app.route('/api/obs/playlist/get', methods=['GET'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def get_playlist(auth_token):
        """
        @api {get} /api/obs/playlist/get OBSPlaylistGet
        @apiVersion 1.1.0
        @apiName OBSPlaylistGet
        @apiGroup StreamSystem
        @apiDescription Get OBS playlist content for replay.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.

        @apiSuccess {String[]} files List of file paths inside the playlist.
        """
        try:
            files = []
            result = send_command_to_obs('GetSourceSettings', {'sourceName': 'RediffPlaylist'})
            if result['status'] == 'error' or 'playlist' not in result['sourceSettings']:
                logging.error(result)
                return jsonify({'success': 'no',
                                'error': 'InternalOBSError',
                                'payload': {}}), 200
            len_path = len(app.config['OBS_PLAYLIST_PATH']) + 1
            for file in result['sourceSettings']['playlist']:
                files.append(file['value'][len_path:])
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {
                                'files': files
                            }}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200

    @app.route('/api/obs/playlist/update', methods=['POST'])
    @secure(app, ['key', 'user'], ['obs_control'])
    def post_playlist_update(auth_token):
        """
        @api {post} /api/obs/playlist/update OBSPlaylistUpdate
        @apiVersion 1.1.0
        @apiName OBSPlaylistUpdate
        @apiGroup StreamSystem
        @apiDescription Set OBS playlist content for replay.

        @apiHeader {String} Authorization 'Bearer <Auth_Token>'
        @apiError (Errors){String} AuthorizationHeaderInvalid Authorization Header is Invalid.
        @apiError (Errors){String} AuthTokenExpired Token has expired, must be refreshed by client.
        @apiError (Errors){String} AuthTokenInvalid Token is invalid, decode is impossible.
        @apiError (Errors){String} ClientAccessImpossible This type of client can't access target endpoint.
        @apiError (Errors){String} ClientAccessRefused Client has no scope access to target endpoint.

        @apiError (Errors){String} OBSInternalError Error communicating to OBS.

        @apiParam {String[]} files List of file paths to build the playlist from.
        @apiError (Errors){String} FilesParameterMissing files is not present in the parameters.
        @apiError (Errors){String} FilesParameterInvalid files is not list of valid file paths.
        @apiError (Errors){String} AtLeastOneFileDoesntExist files is not list of valid file paths.
        """
        data = request.get_json(force=True)

        # files checks
        files = data.get('files', None)
        if files is None:
            return jsonify({'success': 'no',
                            'error': 'FilesParameterMissing',
                            'payload': {}
                            }), 200
        if not isinstance(files, list):
            return jsonify({'success': 'no',
                            'error': 'FilesParameterInvalid',
                            'payload': {}
                            }), 200
        for file in files:
            path = os.path.join(app.config['VOD_PATH'], file)
            if not os.path.isfile(path):
                return jsonify({'success': 'no',
                                'error': 'AtLeastOneFileDoesntExist',
                                'payload': {
                                    'file': file
                                }
                                }), 200
        path_files = [{ 'value': os.path.join(app.config['OBS_PLAYLIST_PATH'], x)} for x in files]

        try:
            result = send_command_to_obs('SetSourceSettings', {'sourceName': 'RediffPlaylist',
                                                               'sourceSettings': {
                                                                   'playlist': path_files
                                                               }})
            if result['status'] == 'error':
                logging.error(result)
                return jsonify({'success': 'no',
                                'error': 'InternalOBSError',
                                'payload': {}}), 200
            return jsonify({'success': 'yes',
                            'error': '',
                            'payload': {

                            }}), 200
        except Exception as e:
            logging.error(e)
            return jsonify({'success': 'no',
                            'error': 'InternalOBSError',
                            'payload': {}}), 200
